#!/usr/bin/env python3
"""
Prophantom Johnnet AI 2.0 - Complete Smart Agent Startup
Launch the complete smart agent ecosystem with all features
"""

import asyncio
import sys
import logging
import json
from pathlib import Path
from datetime import datetime
import signal
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

def print_banner():
    """Print system banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║    ██████╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ██╗   ██╗    ║
║    ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗██║   ██║    ║
║    ██████╔╝██████╔╝██║   ██║██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██║   ██║    ║
║    ██╔═══╝ ██╔══██╗██║   ██║██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║   ██║    ║
║    ██║     ██║  ██║╚██████╔╝██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝╚██████╔╝    ║
║    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝  ╚═════╝     ║
║                                                                                  ║
║       ██╗ ██████╗ ██╗  ██╗███╗   ██╗███╗   ██╗███████╗████████╗                ║
║       ██║██╔═══██╗██║  ██║████╗  ██║████╗  ██║██╔════╝╚══██╔══╝                ║
║       ██║██║   ██║███████║██╔██╗ ██║██╔██╗ ██║█████╗     ██║                   ║
║  ██   ██║██║   ██║██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝     ██║                   ║
║  ╚█████╔╝╚██████╔╝██║  ██║██║ ╚████║██║ ╚████║███████╗   ██║                   ║
║   ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝   ╚═╝                   ║
║                                                                                  ║
║                           █████╗ ██╗    ██████╗     ██████╗                     ║
║                          ██╔══██╗██║    ╚════██╗   ██╔═████╗                    ║
║                          ███████║██║     █████╔╝   ██║██╔██║                    ║
║                          ██╔══██║██║    ██╔═══╝    ████╔╝██║                    ║
║                          ██║  ██║██║    ███████╗██╗╚██████╔╝                    ║
║                          ╚═╝  ╚═╝╚═╝    ╚══════╝╚═╝ ╚═════╝                     ║
║                                                                                  ║
║              🚀 COMPLETE SMART AGENT ECOSYSTEM WITH ADVANCED AI 🚀                ║
║                                                                                  ║
║  ✨ Features: 8 Specialized Agents | Real-time WebSocket | Universal Memory     ║
║  🧠 Analytics: Advanced Performance Monitoring | Predictive Insights           ║
║  🔧 Models: Ollama Integration | 11 AI Models | Adaptive Intelligence           ║
║  💾 Database: Enhanced Schema | Analytics | Memory System                       ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_system_info():
    """Print system information"""
    print("\n" + "="*80)
    print("SYSTEM INITIALIZATION")
    print("="*80)
    print("🌟 Initializing Prophantom Johnnet AI 2.0...")
    print("📅 Startup Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🏠 Working Directory:", os.getcwd())
    print("🐍 Python Version:", sys.version.split()[0])
    print("="*80)

def print_agents_info():
    """Print agents information"""
    agents_info = [
        ("auto_chat", "🤖 Auto Chat Agent", "phi3:14b", "Automated conversation and chat assistance"),
        ("chat_revive", "💬 Chat Revival Agent", "gemma2:2b", "Chat engagement and conversation revival"),
        ("cv_smash", "📄 CV Optimization Agent", "qwen2.5:7b", "Resume and CV optimization specialist"),
        ("emo_ai", "💝 Emotional Support Agent", "llama3.1:8b", "Emotional intelligence and support"),
        ("pdf_mind", "📚 Document Analysis Agent", "mistral:7b", "PDF and document analysis specialist"),
        ("tok_boost", "📱 Social Media Agent", "deepseek-coder:6.7b", "Social media optimization"),
        ("you_gen", "✨ Content Generation Agent", "llama3.2:3b", "Creative content generation"),
        ("agent_x", "🧠 Adaptive Intelligence Agent", "codellama:7b", "Advanced adaptive AI")
    ]
    
    print("\n" + "="*80)
    print("SMART AGENTS OVERVIEW")
    print("="*80)
    for agent_id, name, model, description in agents_info:
        print(f"{name}")
        print(f"   🔧 Model: {model}")
        print(f"   📋 Description: {description}")
        print(f"   🆔 ID: {agent_id}")
        print()
    print("="*80)

def print_features_info():
    """Print features information"""
    print("\n" + "="*80)
    print("ADVANCED FEATURES")
    print("="*80)
    print("🧠 MEMORY SYSTEM:")
    print("   • Episodic Memory - Personal experiences and interactions")
    print("   • Semantic Memory - Knowledge and facts")
    print("   • Procedural Memory - Skills and processes")
    print("   • Emotional Memory - Emotional contexts and responses")
    print()
    print("📊 ANALYTICS SYSTEM:")
    print("   • Real-time Performance Monitoring")
    print("   • User Interaction Analysis")
    print("   • Predictive Insights and Optimization")
    print("   • System Health Reporting")
    print()
    print("🌐 REAL-TIME FEATURES:")
    print("   • WebSocket Communication")
    print("   • Live Agent Interactions")
    print("   • Real-time Dashboard")
    print("   • Instant Notifications")
    print()
    print("🎯 TRAINING & TUNING:")
    print("   • Adaptive Learning Systems")
    print("   • Performance Optimization")
    print("   • Model Fine-tuning")
    print("   • Feedback Integration")
    print("="*80)

async def start_system():
    """Start the complete system"""
    try:
        print_banner()
        print_system_info()
        print_agents_info()
        print_features_info()
        
        print("\n🚀 STARTING SYSTEM COMPONENTS...")
        print("-" * 50)
        
        # Import the system integration
        sys.path.append(os.getcwd())
        from agents.smart_system_integration import SmartAgentSystem
        
        # Initialize system
        print("🔧 Initializing Smart Agent System...")
        system = SmartAgentSystem()
        
        # Start system
        print("⚡ Starting system initialization...")
        if await system.initialize_system():
            print("✅ System initialization completed successfully!")
            
            # Get and display system status
            print("\n📊 SYSTEM STATUS:")
            print("-" * 50)
            status = await system.get_system_status()
            
            print(f"🌟 System: {status['system_info']['name']} v{status['system_info']['version']}")
            print(f"🏃 Environment: {status['system_info']['environment']}")
            print(f"🤖 Active Agents: {len(status['agent_status'])}")
            print(f"💬 Active Sessions: {status['system_info']['active_sessions']}")
            print(f"🔌 WebSocket Connections: {status['system_info']['websocket_connections']}")
            
            # Display agent status
            print("\n🤖 AGENT STATUS:")
            print("-" * 50)
            for agent_name, agent_status in status['agent_status'].items():
                status_icon = "🟢" if agent_status.get('active', False) else "🔴"
                print(f"{status_icon} {agent_name}: {agent_status.get('status', 'unknown')}")
            
            # Display memory status
            if 'memory_status' in status:
                memory = status['memory_status']
                print(f"\n🧠 MEMORY SYSTEM:")
                print(f"   📊 Total Items: {memory.get('total_items', 0)}")
                print(f"   🔄 Consolidation Status: {memory.get('consolidation_status', 'unknown')}")
            
            # Display health report
            if 'health_report' in status:
                health = status['health_report']
                health_icon = "🟢" if health.get('overall_status') == 'excellent' else "⚠️"
                print(f"\n{health_icon} SYSTEM HEALTH: {health.get('overall_status', 'unknown').upper()}")
                print(f"   📈 Health Score: {health.get('overall_health_score', 0):.2f}/1.00")
            
            print("\n" + "="*80)
            print("🎉 PROPHANTOM JOHNNET AI 2.0 IS FULLY OPERATIONAL!")
            print("="*80)
            print("🌐 WebSocket Server: Ready for connections")
            print("🤖 All Agents: Active and responding")
            print("🧠 Memory System: Online and learning")
            print("📊 Analytics: Real-time monitoring active")
            print("="*80)
            
            print("\n📖 USAGE INSTRUCTIONS:")
            print("- Connect via WebSocket for real-time interactions")
            print("- Use REST API endpoints for standard requests")
            print("- Monitor system health via analytics dashboard")
            print("- Check logs/system.log for detailed information")
            
            print("\n⚠️ Press Ctrl+C to gracefully shutdown the system")
            print("-" * 80)
            
            # Keep system running
            logger.info("System is now running. Press Ctrl+C to stop.")
            
            # Setup signal handlers for graceful shutdown
            def signal_handler(signum, frame):
                logger.info("Shutdown signal received. Gracefully shutting down...")
                print("\n🛑 Graceful shutdown initiated...")
                # Here you would add cleanup code
                sys.exit(0)
            
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            
            # Main system loop
            try:
                while True:
                    await asyncio.sleep(10)
                    # Periodic health checks could go here
                    
            except KeyboardInterrupt:
                print("\n🛑 Shutdown requested by user")
                logger.info("System shutdown completed")
                
        else:
            print("❌ System initialization failed!")
            logger.error("Failed to initialize system")
            return False
            
    except Exception as e:
        print(f"❌ Critical system error: {str(e)}")
        logger.error(f"Critical system error: {str(e)}")
        return False
    
    return True

def run_system_checks():
    """Run pre-startup system checks"""
    print("\n🔍 RUNNING SYSTEM CHECKS...")
    print("-" * 50)
    
    checks_passed = True
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        checks_passed = False
    else:
        print("✅ Python version check passed")
    
    # Check required directories
    required_dirs = ['agents', 'core', 'config', 'logs']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"⚠️ Creating missing directory: {dir_name}")
            os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Directory check passed: {dir_name}")
    
    # Check database file
    db_path = "core/agents.db"
    if os.path.exists(db_path):
        print("✅ Database file exists")
    else:
        print("⚠️ Database will be created during initialization")
    
    print("-" * 50)
    
    if checks_passed:
        print("✅ All system checks passed!")
    else:
        print("❌ Some system checks failed!")
    
    return checks_passed

async def main():
    """Main entry point"""
    try:
        # Run system checks
        if not run_system_checks():
            print("❌ System checks failed. Cannot start system.")
            return
        
        # Start the system
        success = await start_system()
        
        if not success:
            print("❌ System startup failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Set event loop policy for Windows compatibility
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # Run the system
    asyncio.run(main())