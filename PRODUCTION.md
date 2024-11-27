# Production Environment

## Backend
### Services
A systemd service has been created to run the backend
To start the service, run the following command:
````bash
sudo systemctl start kpi-backend.service
````

### Logs

Log for backend are located in _/var/logs/kpi/backend/_

- output.log: the output of the backend service
- error.log: errors of the backend service


## Frontend
### Services
A systemd service has been created to run the frontend
To start the service, run the following command:
````bash
sudo systemctl start kpi-frontend.service
````

### Logs

Log for frontend are located in _/var/logs/kpi/frontend/_

- output.log: the output of the service
- error.log: errors of the service