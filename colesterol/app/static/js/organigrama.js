let width = 1000, height = 800;
let svg = d3.select("svg"), g = svg.append("g").attr("transform", "translate(100,100)");
let zoom = d3.zoom().scaleExtent([0.5, 2]).on("zoom", (event) => g.attr("transform", event.transform));
svg.call(zoom);

function actualizarOrganigrama() {
    fetch('/nodos')
        .then(response => response.json())
        .then(data => {
            let hasRoot = data.some(d => d.parent_id === null);
            if (!hasRoot && data.length > 0) data[0].parent_id = null;
            
            let root = d3.stratify().id(d => d.id).parentId(d => d.parent_id)(data);
            let treeLayout = d3.tree().size([width - 200, height - 200]);
            treeLayout(root);
            
            g.selectAll("*").remove();
            
            let links = g.selectAll(".link")
                .data(root.links())
                .enter()
                .append("path")
                .attr("class", d => d.target.data.tipo === "asesoria" ? "link dashed" : "link")
                .attr("d", d => lineaRecta(d))
                .attr("stroke", "black")
                .attr("fill", "none")
              

            g.append("defs").append("marker")
                .attr("id", "arrowhead")
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 35)
                .attr("refY", 0)
                .attr("markerWidth", 6)
                .attr("markerHeight", 6)
                .attr("orient", "auto")
                .append("path")
                .attr("d", "M0,-5L10,0L0,5")
                .attr("fill", "black");

            let nodes = g.selectAll(".node")
                .data(root.descendants())
                .enter()
                .append("g")
                .attr("class", "node")
                .attr("transform", d => `translate(${d.x}, ${d.y})`)
                .call(d3.drag()
                    .on("drag", function(event, d) {
                        d.x += event.dx;
                        d.y += event.dy;
                        d3.select(this).attr("transform", `translate(${d.x}, ${d.y})`);
                        links.attr("d", d => lineaRecta(d));
                        const minDistance = 50; // Distancia mínima entre nodos
                        g.selectAll(".node").each(function(other) {
                            if (other !== d) {
                                const dx = d.x - other.x;
                                const dy = d.y - other.y;
                                const distance = Math.sqrt(dx * dx + dy * dy);
                                if (distance < minDistance) {
                                    d.x -= event.dx; // Revertir movimiento
                                    d.y -= event.dy;
                                }
                            }
                        });
                        fetch(`/nodos/${d.data.id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ x: d.x, y: d.y })
                        });
                    })
                )
                .on("click", (event, d) => {
                    event.stopPropagation();
                    
                    document.getElementById("parentId").value = d.data.id;
                    parentIdInput.value = d.data.id;
                        // Cambiar el color de fondo del campo parentId al color del nodo seleccionado
                    parentIdInput.style.backgroundColor = d.data.color || "#ffffff";
                    d3.select(this).select("rect").attr("stroke", "red").attr("stroke-width", 20);
                    d3.selectAll(".node rect").attr("stroke", "black").attr("stroke-width", 1);
    // Cambiar el color de fondo del campo parentId al color del nodo seleccionado
    
                    // Seleccionar el nodo actual y destacarlo
                    
                })
                .on("dblclick", function(event, d) {
                    event.stopPropagation();
                    let nodo = d3.select(this);
                
                    // Crear contenedor para los inputs y el botón
                    let container = document.createElement("div");
                    container.style.position = "absolute";
                    container.style.left = `${event.pageX}px`;
                    container.style.top = `${event.pageY}px`;
                    container.style.backgroundColor = "#f9f9f9";
                    container.style.border = "1px solid #ccc";
                    container.style.borderRadius = "5px";
                    container.style.padding = "10px";
                    container.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";
                    container.style.zIndex = "1000";
                
                    // Crear input de texto para el nombre
                    let input = document.createElement("input");
                    input.type = "text";
                    input.value = d.data.nombre;
                    input.style.marginBottom = "10px";
                    input.style.width = "100%";
                    input.style.padding = "5px";
                    input.style.border = "1px solid #ccc";
                    input.style.borderRadius = "3px";
                
                    // Crear input de color
                    let colorInput = document.createElement("input");
                    colorInput.type = "color";
                    colorInput.value = d.data.color || "#ffffff";
                    colorInput.style.marginBottom = "10px";
                    colorInput.style.width = "100%";
                    colorInput.style.padding = "5px";
                    colorInput.style.border = "none";
                
                    // Crear botón de confirmación
                    let confirmButton = document.createElement("button");
                    confirmButton.textContent = "✔️ Confirmar";
                    confirmButton.style.backgroundColor = "#4CAF50";
                    confirmButton.style.color = "white";
                    confirmButton.style.border = "none";
                    confirmButton.style.padding = "5px 10px";
                    confirmButton.style.borderRadius = "3px";
                    confirmButton.style.cursor = "pointer";
                    confirmButton.style.width = "100%";
                
                    // Función para guardar los cambios
                    function guardarCambios() {
                        d.data.nombre = input.value;
                        d.data.color = colorInput.value;
                
                        // Actualizar el texto y el color del nodo en el DOM
                        nodo.select("text").text(d.data.nombre);
                        nodo.select("rect").attr("fill", d.data.color);
                
                        // Guardar los cambios en el servidor
                        fetch(`/nodos/${d.data.id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                nombre: d.data.nombre,
                                color: d.data.color
                            })
                        }).then(() => {
                            // Actualizar el organigrama en tiempo real
                            actualizarOrganigrama();
                        });
                
                        // Eliminar el contenedor de los inputs
                        document.body.removeChild(container);
                    }
                
                    // Agregar evento al botón de confirmación
                    confirmButton.addEventListener("click", guardarCambios);
                
                    // Agregar los elementos al contenedor
                    container.appendChild(input);
                    container.appendChild(colorInput);
                    container.appendChild(confirmButton);
                
                    // Agregar el contenedor al documento
                    document.body.appendChild(container);
                
                    // Enfocar el input de texto
                    input.focus();
                
                    // Cerrar el contenedor si se hace clic fuera de él
                    document.addEventListener("click", function cerrar(event) {
                        if (!container.contains(event.target)) {
                            document.body.removeChild(container);
                            document.removeEventListener("click", cerrar);
                        }
                    }, { once: true });
                });
            

                nodes.append("rect")
    .attr("x", d => -calculateTextWidth(d.data.nombre) / 2 - 10) // Ajustar posición en base al ancho del texto
    .attr("y", d => -calculateTextHeight(d.data.nombre) / 2 - 10) // Ajustar posición en base a la altura del texto
    .attr("width", d => calculateTextWidth(d.data.nombre) + 20) // Ajustar ancho dinámicamente
    .attr("height", d => calculateTextHeight(d.data.nombre) + 20) // Ajustar altura dinámicamente
    .attr("rx", 10)
    .attr("ry", 10)
    .attr("fill", d => d.data.color || "#ffffff")
    .attr("stroke", "black");

            let textElement = nodes.append("text")
                .attr("x", 0)
                .attr("y", 5)
                .attr("text-anchor", "middle")
                .attr("class", "node-text")
                .attr("alignment-baseline", "middle")
                .text(d => d.data.nombre)
                
                .style("cursor", "text")
                .style("font-size", "14px")
                .style("white-space", "pre-wrap") // Permitir ajuste de línea
                .style("word-wrap", "break-word") // Dividir palabras largas
                .style("overflow", "hidden")
                .call(wrapText);
                
                g.append("defs")
                .append("clipPath")
                .attr("id", "clip")
                .append("rect")
                .attr("x", -60)
                .attr("y", -20)
                .attr("width", 120)
                .attr("height", 40);
            nodes.append("text")
                .attr("class", "deleteBtn")
                .attr("x", 50)
                .attr("y", -15)
                .text("❌")
                .style("cursor", "pointer")
                .on("click", (event, d) => {
                    event.stopPropagation();
                    fetch('/nodos/' + d.data.id, { method: 'DELETE' })
                        .then(() => actualizarOrganigrama());
                });
        });
}

// Función para calcular el ancho del texto
function calculateTextWidth(text) {
    const tempText = svg.append("text")
        .attr("class", "temp-text")
        .attr("x", -9999) // Posición fuera del viewport
        .attr("y", -9999)
        .text(text)
        .style("font-size", "14px")
        .style("font-family", "Arial");

    const width = tempText.node().getBBox().width;
    tempText.remove();
    return width;
}

// Función para calcular la altura del texto
function calculateTextHeight(text) {
    const tempText = svg.append("text")
        .attr("class", "temp-text")
        .attr("x", -9999) // Posición fuera del viewport
        .attr("y", -9999)
        .text(text)
        .style("font-size", "14px")
        .style("font-family", "Arial")
        .style("white-space", "pre-wrap");

    const height = tempText.node().getBBox().height;
    tempText.remove();
    return height;
}

// Función para ajustar el texto dentro del rectángulo
function wrapText(selection) {
    selection.each(function(d) {
        const text = d3.select(this);
        const words = d.data.nombre.split(/\s+/).reverse();
        const lineHeight = 16; // Altura de línea en píxeles
        const width = calculateTextWidth(d.data.nombre);
        const x = text.attr("x");
        const y = text.attr("y");

        let line = [];
        let lineNumber = 0;
        let tspan = text.text(null).append("tspan").attr("x", x).attr("y", y);

        while (words.length > 0) {
            line.push(words.pop());
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                tspan.text(line.join(" "));
                line = [words.pop()];
                tspan = text.append("tspan")
                    .attr("x", x)
                    .attr("y", ++lineNumber * lineHeight + parseFloat(y))
                    .text(line.join(" "));
            }
        }
    });
}
function lineaRecta(d) {
    return `M${d.source.x},${d.source.y} L${d.source.x},${d.target.y} L${d.target.x},${d.target.y}`;
}

actualizarOrganigrama();

document.getElementById("saveAsPDF").addEventListener("click", function () {
    const canvasContainer = document.getElementById("canvas-container");
    
    // Ocultar las "X" antes de capturar
    document.querySelectorAll(".deleteBtn").forEach(btn => btn.style.display = "none");

    html2canvas(canvasContainer).then(canvas => {
        const imgData = canvas.toDataURL("image/png");
        const pdf = new jspdf.jsPDF("landscape", "mm", "a4");

        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;

        pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
        pdf.save("organigrama.pdf");

        // Restaurar las "X" después de la captura
        document.querySelectorAll(".deleteBtn").forEach(btn => btn.style.display = "block");
    });
});

document.getElementById("saveAsPNG").addEventListener("click", function () {
    const canvasContainer = document.getElementById("canvas-container");

    // Ocultar las "X" antes de capturar
    document.querySelectorAll(".deleteBtn").forEach(btn => btn.style.display = "none");

    html2canvas(canvasContainer).then(canvas => {
        const link = document.createElement("a");
        link.download = "organigrama.png";
        link.href = canvas.toDataURL("image/png");
        link.click();

        // Restaurar las "X" después de la captura
        document.querySelectorAll(".deleteBtn").forEach(btn => btn.style.display = "block");
    });
});

document.getElementById("nodeForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let nombre = document.getElementById("nombre").value;
    let tipo = document.getElementById("tipo").value;
    let forma = document.getElementById("forma").value;
    let color = document.getElementById("color").value;
    let parentId = document.getElementById("parentId").value || null;

    // Verificar si no hay nodos existentes
    const hasNodes = document.querySelectorAll(".node").length > 0;

    // Si no hay nodos, crear un nodo raíz
    if (!hasNodes && !parentId) {
        parentId = null; // Asegurar que el nodo raíz tenga parent_id null
    } else if (!parentId) {
        alert("Por favor, selecciona un nodo antes de agregar uno nuevo.");
        return;
    }

    // Crear el nodo en el servidor
    fetch('/nodos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre, tipo, forma, color, parent_id: parentId })
    }).then(() => {
        actualizarOrganigrama();
        document.getElementById("nodeForm").reset();
    });
});
document.getElementById("clearForm").addEventListener("click", function() {
    document.getElementById("nodeForm").reset();
});
