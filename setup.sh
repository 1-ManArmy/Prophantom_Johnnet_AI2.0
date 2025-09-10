#!/bin/bash

# Prophantom Johnnet AI 2.0 Setup Script
# This script sets up the AI platform with all 9 agents

echo "🚀 Setting up Prophantom Johnnet AI 2.0 - The Sovereign Gateway"
echo "================================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

print_status "Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

print_status "pip3 found: $(pip3 --version)"

# Create virtual environment
print_info "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_info "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Dependencies installed successfully"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p uploads logs templates/auth static/css static/js static/images

# Initialize database
print_info "Initializing database..."
python3 -c "
from app import create_app
from core.database import init_db

app, _ = create_app()
with app.app_context():
    init_db(app)
print('Database initialized successfully')
"

print_status "Database initialized"

# Check if Ollama is running
print_info "Checking Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    print_status "Ollama is running and accessible"
    
    # List available models
    print_info "Available Ollama models:"
    curl -s http://localhost:11434/api/tags | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for model in data.get('models', []):
        print(f'  - {model[\"name\"]} ({model[\"size\"]//1000000}MB)')
except:
    print('  Could not parse model list')
"
else
    print_warning "Ollama is not running or not accessible at localhost:11434"
    print_info "To start Ollama:"
    print_info "  1. Install Ollama: https://ollama.ai/download"
    print_info "  2. Run: ollama serve"
    print_info "  3. Pull models: ollama pull phi3:14b"
fi

# Create a basic .env file
print_info "Creating environment configuration..."
cat > .env << EOF
# Prophantom Johnnet AI 2.0 Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=prophantom-johnnet-ai-2024-secret-key-change-in-production
OLLAMA_HOST=http://localhost:11434
DATABASE_URL=sqlite:///prophantom_ai.db
EOF

print_status "Environment configuration created"

# Create run script
print_info "Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
# Activate virtual environment and run the application
source venv/bin/activate
echo "🚀 Starting Prophantom Johnnet AI 2.0..."
echo "Available at: http://localhost:5000"
echo "Dashboard: http://localhost:5000/dashboard"
echo "Press Ctrl+C to stop"
python3 app.py
EOF

chmod +x run.sh
print_status "Run script created (./run.sh)"

# Display setup summary
echo ""
echo "================================================================"
print_status "Prophantom Johnnet AI 2.0 Setup Complete!"
echo "================================================================"
echo ""
print_info "🏠 Main Application: http://localhost:5000"
print_info "📊 Dashboard: http://localhost:5000/dashboard"
print_info "📚 API Docs: http://localhost:5000/docs"
echo ""
print_info "Available Agents:"
echo "  💖 AI Girlfriend - Companion support (Phi3 14B)"
echo "  😊 EmoAI - Sentiment analysis (Gemma2 2B)"
echo "  📄 PDFMind - Document intelligence (Qwen2.5 7B)"
echo "  💬 ChatRevive - Conversation enhancer (Mistral 7B)"
echo "  🚀 TokBoost - Social media optimizer (Llama3.2 3B)"
echo "  ✨ YouGen - Content generator (DeepSeek-Coder 6.7B)"
echo "  🕵️ AgentX - Multi-domain specialist (Yi 6B)"
echo "  🤖 AutoChat - Automated assistant (Mathstral 7B)"
echo "  💼 CVSmash - Resume optimizer (LLaVA 7B)"
echo ""
print_info "To start the application:"
echo "  ./run.sh"
echo ""
print_info "To run with Docker:"
echo "  docker-compose up -d"
echo ""
print_warning "Make sure Ollama is running with required models!"
echo "================================================================"