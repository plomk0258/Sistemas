# INSTALACIÓN DE LIBRERÍAS
# pip install textblob vaderSentiment pandas matplotlib seaborn wordcloud nltk streamlit plotly

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from wordcloud import WordCloud
import re
from datetime import datetime
import json
import io
from collections import Counter
import numpy as np

# Descargar recursos necesarios de NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class DatasetManager:
    def __init__(self):
        self.dataset = pd.DataFrame()
        self.word_sentiment_dict = {}
        self.dataset_loaded = False
    
    def load_dataset(self, file_data, file_type="csv"):
        """Carga el dataset desde archivo CSV o Excel"""
        try:
            if file_type == "csv":
                self.dataset = pd.read_csv(io.StringIO(file_data.decode('utf-8')))
            elif file_type == "excel":
                self.dataset = pd.read_excel(io.BytesIO(file_data))
            
            # Normalizar nombres de columnas
            self.dataset.columns = self.dataset.columns.str.lower().str.strip()
            
            # Verificar columnas necesarias
            required_cols = ['texto', 'sentimiento']
            if not all(col in self.dataset.columns for col in required_cols):
                # Intentar detectar columnas automáticamente
                text_cols = [col for col in self.dataset.columns if any(word in col for word in ['text', 'comentario', 'mensaje', 'review'])]
                sentiment_cols = [col for col in self.dataset.columns if any(word in col for word in ['sentiment', 'sentimiento', 'label', 'categoria'])]
                
                if text_cols and sentiment_cols:
                    self.dataset = self.dataset.rename(columns={
                        text_cols[0]: 'texto',
                        sentiment_cols[0]: 'sentimiento'
                    })
                else:
                    return False, "El dataset debe tener columnas 'texto' y 'sentimiento' (o similares)"
            
            # Limpiar y normalizar sentimientos
            self.dataset['sentimiento'] = self.dataset['sentimiento'].str.lower().str.strip()
            sentiment_mapping = {
                'positive': 'positivo', 'pos': 'positivo', '1': 'positivo',
                'negative': 'negativo', 'neg': 'negativo', '0': 'negativo', '-1': 'negativo',
                'neutral': 'neutral', 'neu': 'neutral', '2': 'neutral'
            }
            self.dataset['sentimiento'] = self.dataset['sentimiento'].replace(sentiment_mapping)
            
            # Crear diccionario de palabras-sentimiento
            self._create_word_sentiment_dict()
            self.dataset_loaded = True
            
            return True, f"Dataset cargado exitosamente: {len(self.dataset)} comentarios"
            
        except Exception as e:
            return False, f"Error al cargar dataset: {str(e)}"
    
    def _create_word_sentiment_dict(self):
        """Crea un diccionario de palabras y sus sentimientos predominantes"""
        word_sentiment_counts = {}
        
        for _, row in self.dataset.iterrows():
            texto = str(row['texto']).lower()
            sentimiento = row['sentimiento']
            
            # Limpiar texto y extraer palabras
            texto_limpio = re.sub(r'[^\w\s]', '', texto)
            palabras = texto_limpio.split()
            
            for palabra in palabras:
                if len(palabra) > 2:  # Ignorar palabras muy cortas
                    if palabra not in word_sentiment_counts:
                        word_sentiment_counts[palabra] = {'positivo': 0, 'negativo': 0, 'neutral': 0}
                    word_sentiment_counts[palabra][sentimiento] += 1
        
        # Determinar sentimiento predominante para cada palabra
        for palabra, counts in word_sentiment_counts.items():
            if sum(counts.values()) >= 2:  # Mínimo 2 apariciones
                sentimiento_predominante = max(counts, key=counts.get)
                confianza = counts[sentimiento_predominante] / sum(counts.values())
                if confianza >= 0.6:  # Mínimo 60% de confianza
                    self.word_sentiment_dict[palabra] = {
                        'sentimiento': sentimiento_predominante,
                        'confianza': confianza,
                        'apariciones': sum(counts.values())
                    }
    
    def get_dataset_stats(self):
        """Obtiene estadísticas del dataset"""
        if not self.dataset_loaded:
            return None
        
        stats = {
            'total': len(self.dataset),
            'positivo': len(self.dataset[self.dataset['sentimiento'] == 'positivo']),
            'negativo': len(self.dataset[self.dataset['sentimiento'] == 'negativo']),
            'neutral': len(self.dataset[self.dataset['sentimiento'] == 'neutral']),
            'palabras_clave': len(self.word_sentiment_dict)
        }
        return stats
    
    def analyze_with_dataset(self, texto):
        """Analiza texto usando el dataset personalizado"""
        if not self.dataset_loaded:
            return None
        
        texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
        palabras = texto_limpio.split()
        
        sentimientos_encontrados = []
        palabras_encontradas = []
        
        for palabra in palabras:
            if palabra in self.word_sentiment_dict:
                info = self.word_sentiment_dict[palabra]
                sentimientos_encontrados.append(info['sentimiento'])
                palabras_encontradas.append({
                    'palabra': palabra,
                    'sentimiento': info['sentimiento'],
                    'confianza': info['confianza'],
                    'apariciones': info['apariciones']
                })
        
        if not sentimientos_encontrados:
            return {
                'sentimiento_dataset': 'neutral',
                'confianza_dataset': 0.5,
                'palabras_encontradas': [],
                'metodo': 'default'
            }
        
        # Calcular sentimiento final
        contador_sentimientos = Counter(sentimientos_encontrados)
        sentimiento_final = contador_sentimientos.most_common(1)[0][0]
        
        # Calcular confianza promedio
        confianza_promedio = np.mean([p['confianza'] for p in palabras_encontradas])
        
        return {
            'sentimiento_dataset': sentimiento_final,
            'confianza_dataset': confianza_promedio,
            'palabras_encontradas': palabras_encontradas,
            'metodo': 'dataset'
        }

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.comments_history = []
        self.dataset_manager = DatasetManager()
        
    def clean_text(self, text):
        """Limpia el texto de caracteres especiales"""
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()
    
    def analyze_textblob(self, text):
        """Análisis con TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.05:
            return 'positivo', polarity, blob.sentiment.subjectivity
        elif polarity < -0.05:
            return 'negativo', polarity, blob.sentiment.subjectivity
        else:
            return 'neutral', polarity, blob.sentiment.subjectivity
    
    def analyze_vader(self, text):
        """Análisis con VADER"""
        scores = self.vader_analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.02:
            sentiment = 'positivo'
        elif compound <= -0.02:
            sentiment = 'negativo'
        else:
            sentiment = 'neutral'
            
        return sentiment, compound, scores
    
    def analyze_comment(self, text, platform="Web"):
        """Análisis completo de un comentario"""
        cleaned_text = self.clean_text(text)
        
        # Análisis tradicional
        tb_sentiment, tb_polarity, tb_subjectivity = self.analyze_textblob(cleaned_text)
        vader_sentiment, vader_compound, vader_scores = self.analyze_vader(cleaned_text)
        traditional_sentiment = self.combine_results(tb_sentiment, vader_sentiment, tb_polarity, vader_compound)
        
        # Análisis con dataset personalizado
        dataset_result = self.dataset_manager.analyze_with_dataset(text)
        
        # Combinar resultados
        final_sentiment = self.combine_all_results(traditional_sentiment, dataset_result)
        
        result = {
            'text': text,
            'platform': platform,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'final_sentiment': final_sentiment,
            'textblob_sentiment': tb_sentiment,
            'textblob_polarity': tb_polarity,
            'textblob_subjectivity': tb_subjectivity,
            'vader_sentiment': vader_sentiment,
            'vader_compound': vader_compound,
            'vader_scores': vader_scores,
            'dataset_result': dataset_result,
            'confidence': self.calculate_confidence(tb_polarity, vader_compound, dataset_result)
        }
        
        self.comments_history.append(result)
        return result
    
    def combine_results(self, tb_sentiment, vader_sentiment, tb_polarity, vader_compound):
        """Combina resultados de TextBlob y VADER"""
        if tb_sentiment == vader_sentiment:
            return tb_sentiment
        
        if tb_sentiment == 'neutral' and vader_sentiment != 'neutral':
            return vader_sentiment
        elif vader_sentiment == 'neutral' and tb_sentiment != 'neutral':
            return tb_sentiment
        
        if abs(tb_polarity) > abs(vader_compound):
            return tb_sentiment
        else:
            return vader_sentiment
    
    def combine_all_results(self, traditional_sentiment, dataset_result):
        """Combina todos los métodos de análisis"""
        if not dataset_result or dataset_result['metodo'] == 'default':
            return traditional_sentiment
        
        dataset_sentiment = dataset_result['sentimiento_dataset']
        dataset_confidence = dataset_result['confianza_dataset']
        
        # Si el dataset tiene alta confianza, priorizar su resultado
        if dataset_confidence > 0.8:
            return dataset_sentiment
        
        # Si coinciden, usar ese resultado
        if traditional_sentiment == dataset_sentiment:
            return traditional_sentiment
        
        # Si hay discrepancia, usar el del dataset si tiene confianza razonable
        if dataset_confidence > 0.6:
            return dataset_sentiment
        else:
            return traditional_sentiment
    
    def calculate_confidence(self, tb_polarity, vader_compound, dataset_result):
        """Calcula confianza del análisis"""
        traditional_strength = (abs(tb_polarity) + abs(vader_compound)) / 2
        
        if dataset_result and dataset_result['metodo'] == 'dataset':
            dataset_confidence = dataset_result['confianza_dataset']
            combined_confidence = (traditional_strength + dataset_confidence) / 2
        else:
            combined_confidence = traditional_strength
        
        confidence = min(95, max(60, combined_confidence * 100))
        return round(confidence, 1)
    
    def get_statistics(self):
        """Obtiene estadísticas generales"""
        if not self.comments_history:
            return {}
        
        df = pd.DataFrame(self.comments_history)
        stats = {
            'total': len(df),
            'positivo': len(df[df['final_sentiment'] == 'positivo']),
            'negativo': len(df[df['final_sentiment'] == 'negativo']),
            'neutral': len(df[df['final_sentiment'] == 'neutral']),
            'avg_confidence': df['confidence'].mean(),
            'platforms': df['platform'].value_counts().to_dict()
        }
        return stats

def main():
    st.set_page_config(
        page_title="Analizador de Sentimientos con Dataset",
        page_icon="💬",
        layout="wide"
    )
    
    st.title("🤖 Analizador de Sentimientos con Dataset ")
    st.markdown("### Análisis automático usando dataset ")
    
    # Inicializar analizador
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = SentimentAnalyzer()
    
    analyzer = st.session_state.analyzer
    
    # Sidebar para dataset
    with st.sidebar:
        st.header("📊 Gestión de Dataset")
        
        # Cargar dataset
        uploaded_file = st.file_uploader(
            "Sube tu dataset (CSV o Excel)",
            type=['csv', 'xlsx', 'xls'],
            help="El archivo debe tener columnas 'texto' y 'sentimiento'"
        )
        
        if uploaded_file is not None:
            file_type = "csv" if uploaded_file.name.endswith('.csv') else "excel"
            
            if st.button("📁 Cargar Dataset"):
                with st.spinner("Cargando dataset..."):
                    success, message = analyzer.dataset_manager.load_dataset(
                        uploaded_file.getvalue(), file_type
                    )
                
                if success:
                    st.success(message)
                else:
                    st.error(message)
                
                st.rerun()
        
        # Mostrar estadísticas del dataset
        if analyzer.dataset_manager.dataset_loaded:
            st.success("✅ Dataset cargado")
            stats = analyzer.dataset_manager.get_dataset_stats()
            
            st.metric("Total comentarios", stats['total'])
            st.metric("Palabras clave", stats['palabras_clave'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Positivos", stats['positivo'])
            with col2:
                st.metric("Negativos", stats['negativo'])
            with col3:
                st.metric("Neutrales", stats['neutral'])
        else:
            st.info("📝 Sube un dataset para análisis personalizado")
            
            # Crear dataset de ejemplo
            if st.button("📄 Crear Dataset de Ejemplo"):
                ejemplo_data = {
                    'texto': [
                        'Excelente producto, muy recomendado',
                        'Pésimo servicio, muy decepcionado',
                        'El producto está bien, cumple su función',
                        'Increíble calidad, superó mis expectativas',
                        'Malo, no funciona como esperaba',
                        'Bueno, precio justo',
                        'Fantástico, lo mejor que he comprado',
                        'Terrible experiencia, no lo recomiendo',
                        'Correcto, sin más',
                        'Maravilloso, cinco estrellas'
                    ],
                    'sentimiento': [
                        'positivo', 'negativo', 'neutral', 'positivo', 'negativo',
                        'neutral', 'positivo', 'negativo', 'neutral', 'positivo'
                    ]
                }
                
                df_ejemplo = pd.DataFrame(ejemplo_data)
                csv_ejemplo = df_ejemplo.to_csv(index=False)
                
                st.download_button(
                    label="📥 Descargar Dataset de Ejemplo",
                    data=csv_ejemplo,
                    file_name="dataset_ejemplo.csv",
                    mime="text/csv"
                )
        
        st.markdown("---")
        
        # Configuración adicional
        platform = st.selectbox(
            "Plataforma:",
            ["Twitter", "Facebook", "Instagram", "LinkedIn", "YouTube", "Web"]
        )
        
        if st.button("🗑️ Limpiar Historial"):
            st.session_state.analyzer = SentimentAnalyzer()
            st.success("¡Historial limpiado!")
            st.rerun()
    
    # Layout principal
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Analizar Nuevo Comentario")
        
        user_input = st.text_area(
            "Escribe o pega un comentario:",
            height=100,
            placeholder="Ejemplo: Este producto es fantástico y lo recomiendo..."
        )
        
        if st.button("🔍 Analizar Sentimiento", type="primary"):
            if user_input.strip():
                with st.spinner("Analizando comentario..."):
                    result = analyzer.analyze_comment(user_input, platform)
                
                # Mostrar resultado
                sentiment_colors = {
                    'positivo': '🟢',
                    'negativo': '🔴',
                    'neutral': '🟡'
                }
                
                st.success(f"**Análisis completado!**")
                st.write(f"**Sentimiento Final:** {sentiment_colors[result['final_sentiment']]} {result['final_sentiment'].title()}")
                st.write(f"**Confianza:** {result['confidence']}%")
                
                # Mostrar análisis detallado
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write("**Métodos Tradicionales:**")
                    st.write(f"TextBlob: {result['textblob_sentiment']}")
                    st.write(f"VADER: {result['vader_sentiment']}")
                
                with col_b:
                    if result['dataset_result'] and result['dataset_result']['metodo'] == 'dataset':
                        st.write("**Análisis con Dataset:**")
                        st.write(f"Resultado: {result['dataset_result']['sentimiento_dataset']}")
                        st.write(f"Confianza: {result['dataset_result']['confianza_dataset']:.2f}")
                    else:
                        st.write("**Dataset:**")
                        st.write("No aplicado")
                
                # Mostrar palabras encontradas en el dataset
                if (result['dataset_result'] and 
                    result['dataset_result']['palabras_encontradas']):
                    
                    st.write("**Palabras clave encontradas en tu dataset:**")
                    for palabra_info in result['dataset_result']['palabras_encontradas']:
                        st.write(f"• **{palabra_info['palabra']}**: {palabra_info['sentimiento']} "
                               f"(confianza: {palabra_info['confianza']:.2f})")
                
                st.rerun()
            else:
                st.warning("Por favor, ingresa un comentario para analizar.")
        
        # Pruebas con el dataset
        if analyzer.dataset_manager.dataset_loaded:
            st.markdown("**🧪 Probar con palabras de tu dataset:**")
            
            # Obtener algunas palabras del dataset
            sample_words = list(analyzer.dataset_manager.word_sentiment_dict.keys())[:5]
            
            for word in sample_words:
                word_info = analyzer.dataset_manager.word_sentiment_dict[word]
                if st.button(f"Probar: '{word}' → {word_info['sentimiento']}", key=f"word_{word}"):
                    result = analyzer.analyze_comment(f"Esto es {word}", platform)
                    st.write(f"→ {result['final_sentiment']} ({result['confidence']}%)")
    
    with col2:
        st.subheader("📊 Estadísticas en Tiempo Real")
        
        stats = analyzer.get_statistics()
        
        if stats:
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                st.metric("Total", stats['total'])
            with col_b:
                st.metric("Positivos", stats['positivo'])
            with col_c:
                st.metric("Negativos", stats['negativo'])
            with col_d:
                st.metric("Neutrales", stats['neutral'])
            
            if stats['total'] > 0:
                fig = px.bar(
                    x=['Positivo', 'Negativo', 'Neutral'],
                    y=[stats['positivo'], stats['negativo'], stats['neutral']],
                    color=['Positivo', 'Negativo', 'Neutral'],
                    color_discrete_map={
                        'Positivo': '#10B981',
                        'Negativo': '#EF4444',
                        'Neutral': '#F59E0B'
                    }
                )
                fig.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Agrega comentarios para ver estadísticas")
    
    # Mostrar dataset cargado
    if analyzer.dataset_manager.dataset_loaded:
        st.subheader("📋 Tu Dataset")
        
        tab1, tab2 = st.tabs(["Vista Previa", "Palabras Clave"])
        
        with tab1:
            st.dataframe(analyzer.dataset_manager.dataset.head(10))
        
        with tab2:
            st.write("**Principales palabras clave extraídas:**")
            
            # Mostrar las palabras más relevantes
            word_items = list(analyzer.dataset_manager.word_sentiment_dict.items())
            word_items.sort(key=lambda x: x[1]['apariciones'], reverse=True)
            
            for word, info in word_items[:20]:  # Top 20
                col_word, col_sent, col_conf, col_count = st.columns([3, 2, 2, 1])
                
                with col_word:
                    st.write(f"**{word}**")
                with col_sent:
                    color = "🟢" if info['sentimiento'] == 'positivo' else "🔴" if info['sentimiento'] == 'negativo' else "🟡"
                    st.write(f"{color} {info['sentimiento']}")
                with col_conf:
                    st.write(f"{info['confianza']:.2f}")
                with col_count:
                    st.write(f"{info['apariciones']}")
    
    # Historial de comentarios
    if analyzer.comments_history:
        st.subheader("📋 Historial de Comentarios")
        
        for comment in reversed(analyzer.comments_history[-5:]):  # Últimos 5
            with st.container():
                col_icon, col_content = st.columns([1, 9])
                
                with col_icon:
                    if comment['final_sentiment'] == 'positivo':
                        st.write("🟢")
                    elif comment['final_sentiment'] == 'negativo':
                        st.write("🔴")
                    else:
                        st.write("🟡")
                
                with col_content:
                    st.write(f"**{comment['text']}**")
                    
                    # Mostrar si se usó el dataset
                    dataset_used = (comment['dataset_result'] and 
                                  comment['dataset_result']['metodo'] == 'dataset')
                    
                    dataset_indicator = "📊 Dataset" if dataset_used else "🔧 Tradicional"
                    
                    st.caption(f"{comment['platform']} • {comment['timestamp']} • "
                             f"Confianza: {comment['confidence']}% • {dataset_indicator}")
                
                st.divider()

if __name__ == "__main__":
    main()