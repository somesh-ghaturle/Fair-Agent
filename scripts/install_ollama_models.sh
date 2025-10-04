#!/bin/bash
# Ollama Model Installer for FAIR-Agent
# Downloads recommended models for medical and finance domains

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║        FAIR-Agent Ollama Model Installer                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Error: Ollama is not installed!"
    echo ""
    echo "Please install Ollama first:"
    echo "  macOS:   brew install ollama"
    echo "  Linux:   curl -fsSL https://ollama.com/install.sh | sh"
    echo ""
    exit 1
fi

# Check if Ollama server is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Warning: Ollama server is not running!"
    echo ""
    echo "Starting Ollama server..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
    
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "❌ Error: Could not start Ollama server"
        echo "Please start it manually: ollama serve"
        exit 1
    fi
    echo "✅ Ollama server started"
fi

echo "✅ Ollama is installed and running"
echo ""

# Show currently installed models
echo "📦 Currently installed models:"
ollama list
echo ""

# Function to install a model with progress
install_model() {
    local model_name=$1
    local description=$2
    local size=$3
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📥 Downloading: $description"
    echo "   Model: $model_name"
    echo "   Size: ~$size"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if ollama list | grep -q "$model_name"; then
        echo "✅ Already installed: $model_name"
        return 0
    fi
    
    echo "⏳ Downloading $model_name (this may take several minutes)..."
    if ollama pull "$model_name"; then
        echo "✅ Successfully installed: $model_name"
        return 0
    else
        echo "❌ Failed to install: $model_name"
        return 1
    fi
}

# Interactive menu
show_menu() {
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║              Select Models to Install                         ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Choose an installation option:"
    echo ""
    echo "  1) 🏥 Medical Specialists (~12GB)"
    echo "     - Meditron 7B"
    echo "     - BioMistral 7B"
    echo "     - MedLlama2 7B"
    echo ""
    echo "  2) 💰 Finance Specialists (~12GB)"
    echo "     - Llama 3.1 8B"
    echo "     - Mistral 7B"
    echo "     - Phi-3 Medium"
    echo ""
    echo "  3) 🌟 Top General Purpose (~15GB)"
    echo "     - Gemma 2 9B"
    echo "     - Qwen 2.5 7B"
    echo "     - DeepSeek R1 7B"
    echo ""
    echo "  4) ⚡ Fast & Small Models (~7GB)"
    echo "     - Phi-3.5"
    echo "     - Gemma 2 2B"
    echo "     - Llama 3.2 1B"
    echo ""
    echo "  5) 🎯 Essential Pack (Medical + Finance, ~25GB)"
    echo "     - All medical specialists"
    echo "     - All finance specialists"
    echo ""
    echo "  6) 📦 Complete Collection (ALL, ~60GB)"
    echo "     - Everything above"
    echo ""
    echo "  7) 🔧 Custom - Choose individual models"
    echo ""
    echo "  0) Exit"
    echo ""
    read -p "Enter your choice (0-7): " choice
    echo ""
    return $choice
}

# Medical models
install_medical_models() {
    echo "🏥 Installing Medical Specialist Models..."
    echo ""
    install_model "meditron:latest" "Meditron 7B (Medical Specialist)" "4.1GB"
    echo ""
    install_model "biomistral:latest" "BioMistral 7B (Biomedical Expert)" "4.1GB"
    echo ""
    install_model "medllama2:latest" "MedLlama2 7B (Clinical Focus)" "3.8GB"
    echo ""
}

# Finance models
install_finance_models() {
    echo "💰 Installing Finance Specialist Models..."
    echo ""
    install_model "llama3.1:8b" "Llama 3.1 8B (Enhanced Reasoning)" "4.7GB"
    echo ""
    install_model "mistral:latest" "Mistral 7B (Fast & Accurate)" "4.1GB"
    echo ""
    install_model "phi3:latest" "Phi-3 Medium (Efficient Reasoning)" "3.8GB"
    echo ""
}

# General purpose models
install_general_models() {
    echo "🌟 Installing Top General Purpose Models..."
    echo ""
    install_model "gemma2:9b" "Gemma 2 9B (Google)" "5.5GB"
    echo ""
    install_model "qwen2.5:7b" "Qwen 2.5 7B (Alibaba)" "4.7GB"
    echo ""
    install_model "deepseek-r1:7b" "DeepSeek R1 7B" "4.7GB"
    echo ""
}

# Fast models
install_fast_models() {
    echo "⚡ Installing Fast & Small Models..."
    echo ""
    install_model "phi3.5:latest" "Phi-3.5" "3.8GB"
    echo ""
    install_model "gemma2:2b" "Gemma 2 2B" "1.6GB"
    echo ""
    install_model "llama3.2:1b" "Llama 3.2 1B" "1.3GB"
    echo ""
}

# Custom selection
install_custom_models() {
    echo "🔧 Custom Model Selection"
    echo ""
    echo "Available models:"
    echo "  1) Meditron 7B (4.1GB) - Medical"
    echo "  2) BioMistral 7B (4.1GB) - Biomedical"
    echo "  3) MedLlama2 7B (3.8GB) - Clinical"
    echo "  4) Llama 3.1 8B (4.7GB) - Finance/Reasoning"
    echo "  5) Mistral 7B (4.1GB) - Fast reasoning"
    echo "  6) Phi-3 (3.8GB) - Efficient"
    echo "  7) Gemma 2 9B (5.5GB) - Google"
    echo "  8) Qwen 2.5 7B (4.7GB) - Alibaba"
    echo "  9) DeepSeek R1 7B (4.7GB)"
    echo " 10) Phi-3.5 (3.8GB) - Fast"
    echo " 11) Gemma 2 2B (1.6GB) - Very fast"
    echo " 12) Llama 3.2 1B (1.3GB) - Fastest"
    echo ""
    read -p "Enter model numbers separated by spaces (e.g., 1 4 7): " models
    echo ""
    
    for num in $models; do
        case $num in
            1) install_model "meditron:latest" "Meditron 7B" "4.1GB" ;;
            2) install_model "biomistral:latest" "BioMistral 7B" "4.1GB" ;;
            3) install_model "medllama2:latest" "MedLlama2 7B" "3.8GB" ;;
            4) install_model "llama3.1:8b" "Llama 3.1 8B" "4.7GB" ;;
            5) install_model "mistral:latest" "Mistral 7B" "4.1GB" ;;
            6) install_model "phi3:latest" "Phi-3" "3.8GB" ;;
            7) install_model "gemma2:9b" "Gemma 2 9B" "5.5GB" ;;
            8) install_model "qwen2.5:7b" "Qwen 2.5 7B" "4.7GB" ;;
            9) install_model "deepseek-r1:7b" "DeepSeek R1 7B" "4.7GB" ;;
            10) install_model "phi3.5:latest" "Phi-3.5" "3.8GB" ;;
            11) install_model "gemma2:2b" "Gemma 2 2B" "1.6GB" ;;
            12) install_model "llama3.2:1b" "Llama 3.2 1B" "1.3GB" ;;
            *) echo "⚠️  Invalid selection: $num" ;;
        esac
        echo ""
    done
}

# Main installation loop
while true; do
    show_menu
    choice=$?
    
    case $choice in
        1) install_medical_models ;;
        2) install_finance_models ;;
        3) install_general_models ;;
        4) install_fast_models ;;
        5) 
            install_medical_models
            install_finance_models
            ;;
        6)
            install_medical_models
            install_finance_models
            install_general_models
            install_fast_models
            ;;
        7) install_custom_models ;;
        0) 
            echo "👋 Exiting installer"
            break
            ;;
        *)
            echo "❌ Invalid choice. Please try again."
            echo ""
            continue
            ;;
    esac
    
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                    Installation Summary                       ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    ollama list
    echo ""
    
    read -p "Press Enter to continue or Ctrl+C to exit..."
done

echo ""
echo "✅ Installation complete!"
echo ""
echo "📊 Currently installed models:"
ollama list
echo ""
echo "🌐 Next steps:"
echo "  1. Restart FAIR-Agent Django server (if running)"
echo "  2. Open http://localhost:8000/query/ in your browser"
echo "  3. Select a model from the dropdown"
echo "  4. Test it with a query!"
echo ""
echo "📖 For more information, see: OLLAMA_MODELS_GUIDE.md"
echo ""
