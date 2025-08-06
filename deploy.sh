#!/bin/bash
# 🚀 Script de Deploy Automático para Lead Generator Pro

echo "🚀 INICIANDO DEPLOY AUTOMÁTICO"
echo "================================"

# Verificar que estamos en el directorio correcto
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ Error: No se encontró streamlit_app.py"
    echo "   Ejecuta este script desde el directorio del proyecto"
    exit 1
fi

# Verificar que git está configurado
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git no está instalado"
    exit 1
fi

echo "✅ Verificación inicial completada"

# Función para pedir el nombre de usuario de GitHub
get_github_username() {
    read -p "📝 Ingresa tu nombre de usuario de GitHub: " github_username
    if [ -z "$github_username" ]; then
        echo "❌ Error: Nombre de usuario no puede estar vacío"
        exit 1
    fi
    echo "✅ Usuario de GitHub: $github_username"
}

# Función para configurar el remote de GitHub
setup_github_remote() {
    echo "🔗 Configurando repositorio remoto..."
    
    # Remover remote existente si existe
    git remote remove origin 2>/dev/null || true
    
    # Agregar nuevo remote
    git remote add origin "https://github.com/$github_username/lead-generator-pro.git"
    
    if [ $? -eq 0 ]; then
        echo "✅ Repositorio remoto configurado"
    else
        echo "❌ Error configurando repositorio remoto"
        exit 1
    fi
}

# Función para pushear a GitHub
push_to_github() {
    echo "📤 Subiendo código a GitHub..."
    
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Código subido exitosamente a GitHub"
    else
        echo "❌ Error subiendo código a GitHub"
        echo "💡 Asegúrate de que el repositorio existe en GitHub:"
        echo "   https://github.com/$github_username/lead-generator-pro"
        exit 1
    fi
}

# Función para mostrar instrucciones de Streamlit Cloud
show_streamlit_instructions() {
    echo ""
    echo "🌟 PRÓXIMOS PASOS - STREAMLIT CLOUD"
    echo "=================================="
    echo "1. 🌐 Ve a: https://share.streamlit.io"
    echo "2. 🔑 Inicia sesión con tu cuenta de GitHub"
    echo "3. ➕ Clic en 'New app'"
    echo "4. 📋 Selecciona el repositorio: lead-generator-pro"
    echo "5. ⚙️ Configurar:"
    echo "   - Branch: main"
    echo "   - Main file: streamlit_app.py"
    echo "   - App URL: lead-generator-pro"
    echo "6. 🔐 En 'Advanced settings' > 'Secrets', copia el contenido de:"
    echo "   📁 DEPLOYMENT_GUIDE.md (sección 4)"
    echo "7. 🚀 Clic en 'Deploy!'"
    echo ""
    echo "🎯 Tu app estará en: https://lead-generator-pro.streamlit.app"
    echo ""
    echo "📖 Guía completa: cat DEPLOYMENT_GUIDE.md"
}

# Función principal
main() {
    echo "🎯 Lead Generator Pro - Deploy Automático"
    echo ""
    
    # Verificar commits pendientes
    if ! git diff --quiet || ! git diff --cached --quiet; then
        echo "⚠️  Hay cambios sin commitear"
        echo "📝 Haciendo commit automático..."
        git add .
        git commit -m "🚀 Automatic deployment commit $(date)"
    fi
    
    # Obtener username de GitHub
    get_github_username
    
    # Configurar repositorio remoto
    setup_github_remote
    
    # Pushear a GitHub
    push_to_github
    
    # Mostrar instrucciones finales
    show_streamlit_instructions
    
    echo "✅ DEPLOY PREPARADO EXITOSAMENTE!"
    echo "🎉 ¡Tu aplicación está lista para Streamlit Cloud!"
}

# Ejecutar función principal
main 