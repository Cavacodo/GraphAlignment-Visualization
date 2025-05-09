@echo "Running..."
start "" redis-server
start "" rabbitmq-server
start "" neo4j console
start "" cmd /k "cd /d .\FrontEnd\xjtu_frontend && npm run dev"
timeout /t 2
start "" cmd /k "cd .\Align_Algorithm && conda activate base && python mqsever.py"
start "" cmd /k "cd .\BackEnd && mvn spring-boot:run"
pause