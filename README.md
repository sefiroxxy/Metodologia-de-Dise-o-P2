# Metodologia de Diseño P2
Es el proyecto 2 con sus cambios y operaciones respectivas

Integrantes:
- Latuz Zepeda
- Maycol Zincker
- Dietrich Ganz

Estructura del archivo: 

C:\USERS\P2MODFINAL
└───app
    │   main.py
    │   
    ├───application
    │   │   __init__.py
    │   │   
    │   ├───middleware
    │   │       __init__.py
    │   │       
    │   └───services
    │           cliente_servicio.py
    │           pago_servicio.py
    │           pedido_servicio.py
    │           producto_servicio.py
    │           __init__.py
    │           
    ├───core
    │   │   __init__.py
    │   │   
    │   ├───entities
    │   │       cliente.py
    │   │       pago.py
    │   │       pedido.py
    │   │       producto.py
    │   │       __init__.py
    │   │       
    │   └───ports
    │       │   __init__.py
    │       │   
    │       ├───external_services
    │       │       __init__.py
    │       │       
    │       └───repositories
    │               cliente_repositorio_base.py
    │               pago_repositorio_base.py
    │               pedido_repositorio_base.py
    │               producto_repositorio_base.py
    │               __init__.py
    │               
    ├───infrastructure
    │   │   __init__.py
    │   │   
    │   ├───adapters
    │   │   │   __init__.py
    │   │   │   
    │   │   ├───database
    │   │   │       database.py
    │   │   │       __init__.py
    │   │   │       
    │   │   ├───dependency
    │   │   │       dependencies.py
    │   │   │       __init__.py
    │   │   │       
    │   │   ├───external_services
    │   │   │       __init__.py
    │   │   │       
    │   │   ├───handlers
    │   │   │       cliente_handler.py
    │   │   │       handler_health_check.py
    │   │   │       pago_handler.py
    │   │   │       pedido_handler.py
    │   │   │       producto_handler.py
    │   │   │       __init__.py
    │   │   │       
    │   │   ├───repositories
    │   │   │       cliente_repositorio.py
    │   │   │       pago_repositorio.py
    │   │   │       pedido_repositorio.py
    │   │   │       producto_repositorio.py
    │   │   │       __init__.py
    │   │   │       
    │   │   ├───schemas
    │   │   │       cliente_esquema.py
    │   │   │       pago_esquema.py
    │   │   │       pedido_esquema.py
    │   │   │       producto_esquema.py
    │   │   │       __init__.py
    │   │   │       
    │   │   └───web
    │   │           fastapi_adapter.py
    │   │           __init__.py
    │   │           
    │   └───config
    │           logging_config.py
    │           __init__.py
    │           
    ├───test
    │       cliente.py
    │       pago.py
    │       pedido.py
    │       producto.py
    │       repositorio_cliente.py
    │       repositorio_pedido.py
    │       repositorio_producto.py
    │       __init__.py
    │       
    └───utils
            log.py
            __init__.py


Requerimientos para usar:
pip install fastapi==0.115.0
pip install pyctuator==1.0.1
pip install uvicorn[standard]==0.20.0
pip install requests==2.32.3
pip install pydantic~=2.10.2
pip install starlette~=0.38.6

