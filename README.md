# Tarea 1 - Documentacion: Preparando el entorno de trabajo en nuestra computadora 

Llevaremos acabo la instalacion de todo el software requerido para el curso de AWS Data.
Para poder instalar de forma correcta lo que necesitamos tendremos que iniciar abriendo una terminal (PowerShell si
estamos en Windows) en la computadora para ejecutar los comandos requeridos para ir instalando los distintos 
softwares necesarios. Se recomienda abrir PowerShell en modo administrador, empecemos.

## 1. Instalar WSL (Windows Subsystem for Linux) y Ubuntu
Siguiendo las instrucciones que nos brinda la documentacion de Microsoft, ejecutaremos los siguientes comandos en
orden para poder instalar WSL (Windows Subsystem for Linux) y Ubuntu. Con este primer comando vamos a instalar WSL, ademas de activar todas las funciones 
necesarias para ejecutar WSL e instalar la distribucion de Linux llamada Ubuntu.

```bash
wsl --install
```

Nota: Cabe recalcar que la distribucion de Linux que se instala por defecto es Ubuntu, sin embargo, existe la posibilidad de instalar otra 
distribucion de Linux ejecutando el siguiente comando:

### 1.1 Instalar otra distribucion de Linux

```bash
wsl.exe --install -d [Distro]
```

Tendremos que especificar la distribucion de Linux que queremos instalar. Por otro lado, si queremos ver una lista de 
distribuciones disponibles de Linux para descargar desde la tienda podemos ejecutar el siguiente comando:

### 1.2 Ver la lista de distribuciones de Linux disponibles

```bash
wsl.exe --list --online
```

NOTA: Recordemos que todos estos pasos los estamos realizando desde una computadora con SO Windows en nuestra 
PoweShell, tambien es importante mencionar que la distribucion que seleccionamos fue Ubuntu, esa sera 
nuestra distribucion de Linux de ahora en adelante.

Siguiendo los pasos anteriores de forma correcta, ya podremos usar WSL junto con Ubuntu desde nuestra terminal de
Windows sin ningun problema.

Para concluir esta parte y como una buena practica ejecutaremos el siguiente comando: 

```bash
sudo apt update && sudo apt upgrade -y
```

El comando anterior lo debemos de ejecutar una vez que hayamos instalado WSL, este comando tiene dos funciones 
principales muy importantes:
+ La primera funcion es refrescar la lista de paquetes disponibles y sus versiones desde los repositorios. 
+ La segunda funcion es instalar las versiones mas recientes de los paquetes que ya tenemos. 
Con esto nos aseguramos que nuestro sistema este al dia y evitamos conflictos al instalar software nuevo 
(que es justo lo que realizaremos mas adelante). 

---

## 2. Comandos para instalar y configurar Docker Engine
Siguiendo la documentacion de dockerdocs, vamos a instalar Docker Engine utilizando los comandos que se nos indican
tal cual aparecen en la documentacion. La forma recomendada de ejecutar los comandos es ir uno por uno, sin embargo,
tambien es posible copiar los comandos por bloques y ejecutarlos al mismo tiempo.

### 2.1 Primer bloque de comandos - Add Docker's official GPG key

```bash
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

### 2.2 Segundo bloque de comandos - Add the repository to Apt sources

```bash
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```

### 2.3 Instalar los paquetes de docker

```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Una vez que ya tenemos todo instalado, tenemos que realizar algunas verificaciones para asegurarnos de que Docker esta
funcionando correctamente y que la instalacion fue exitosa, para esto vamos a ejecutar los siguientes comandos:

### 2.4 Verificacion del estado de docker

```bash
sudo systemctl status docker
```

<img width="1172" height="332" alt="image" src="https://github.com/user-attachments/assets/4ef708e2-7638-45dd-ad5e-622af5e0ef07" />

Lo que debe de mostrarnos en la terminal es que Docker esta corriendo (running), en el caso de que no sea asi, que 
Docker se encuentre detenido, tendremos que ejecutar el siguiente comando:

### 2.5 Iniciar docker

```bash
sudo systemctl start docker
```

### 2.6 Correr una imagen de prueba y ejecutarla dentro de un contenedor

```bash
sudo docker run hello-world
```

<img width="1030" height="608" alt="image" src="https://github.com/user-attachments/assets/37daf005-0200-4381-9fc0-8d8447ec020d" />

Con el comando anterior, descargamos una imagen de prueba y la ejecutamos dentro de un contenedor. Cuando el 
contenedor se ejecuta, muestra un mensaje de confirmacion, que en este caso sera el famoso hello-world y se cerrara el 
mensaje, esto nos indica que todo el proceso de instalacion que realizamos fue exitoso.

### Pasos posteriores de la instalacion de Docker Engine en nuestra distribucion de Linux
Este es un proceso opcional que podemos realizar despues de la instalacion de Docker Engine dentro de Linux,
dicho proceso nos va a describir como configurar nuestra maquina host Linux para que funcione de mejor manera 
con Docker. Para realizar esto tendremos que seguir los siguientes pasos ejecutando sus respectivos comandos:

### Paso 1: Crear el docker group
```bash
sudo groupadd docker
```

### Paso 2: Agregar tu usuario al docker group
```bash
sudo usermod -aG docker $USER
```

### Paso 3: Aplicar los cambios a los grupos 
```bash
newgrp docker
```

Ahora tenemos que verificar que podemos ejecutar comandos de docker sin la necesidad de usar el sudo, para esto 
ejecutamos el siguiente comando:

```bash
docker run hello-world
```

<img width="982" height="112" alt="image" src="https://github.com/user-attachments/assets/4b174606-410b-41d9-a435-0aa480361766" />


Como ya vimos anteriormente, lo que va a suceder al momento de ejecutar el comando anterior es que se va a descargar
una imagen de prueba y la va a ejecutar dentro de un contenedor. El punto de volver a ejecutar el comando es probar que funciona sin la necesidad
de usar el sudo.

---

## 3. Comandos para la instalacion y configuracion de zsh, Python, pyenv y Jupyter Notebook
Con los siguientes comandos vamos a poder instalar y configurar nuestro entorno para usar zsh, Python, pyenv y Jupyter 
Notebook en nuestra distribucion Linux (Ubuntu en nuestro caso). Sigamos los siguientes comandos para llevar 
acabo este cometido.

### 3.1 Instalar zsh

```bash
sudo apt install -y zsh
```

### 3.2 Instalar oh-my-zsh

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

<img width="1246" height="570" alt="image" src="https://github.com/user-attachments/assets/62257b19-83c7-4547-bd1c-2138a3646c26" />

### 3.3 Instalar las dependencias necesarias 
```bash
sudo apt install -y \
  make \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  curl \
  llvm \
  libncursesw5-dev \
  xz-utils \
  tk-dev \
  libxml2-dev \
  libxmlsec1-dev \
  libffi-dev \
  liblzma-dev
```

Con el comando anterior, instalamos todas las herramientas y bibliotecas necesarias para compilar Python mediante pyenv

### 3.4 Clonar el proyecto pyenv

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

<img width="1032" height="182" alt="image" src="https://github.com/user-attachments/assets/57fe4cbe-f515-4e3b-a733-bc67aacb7103" />

### 3.5 Comprobar que pyenv fue descargado correctamente

```bash
ls ~/.pyenv
```

<img width="1182" height="97" alt="image" src="https://github.com/user-attachments/assets/64d6d969-d745-4c04-8fdf-681e723cf899" />

### 3.6 Configurar pyenv para zsh y comprobar que pyenv funciona 

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc
pyenv --version
```

### 3.7 Consultar las versiones de python disponibles

```bash
pyenv install --list | grep " 3.14"
```

<img width="557" height="442" alt="image" src="https://github.com/user-attachments/assets/24215801-a97f-41b6-b78c-777ec90bc639" />

Con grep filtramos los resultados para mostrar unicamente las versiones correspondientes a Python 3.14, esto nos 
permite comprobar que la version que queremos instalar esta disponible 

### 3.8 Instalar python 3.14.7

```bash
pyenv install 3.14.7
```

<img width="1088" height="458" alt="image" src="https://github.com/user-attachments/assets/6c5d1bfc-bcb6-4b28-92ba-2dde56d2a813" />

### 3.9 Comprobar las versiones administradas por pyenv

```bash
pyenv versions
```

Este comando nos va a mostrar las versiones de Python que pyenv tiene instaladas.

### 3.10 Seleccionar Python 3.14.7 como la version global 

```bash
pyenv global 3.14.7
```

### 3.11 Actualizar los ejecutables de pyenv

```bash
pyenv rehash
```

### 3.12 Verificar la version de Python

```bash
python --version
```

### 4. Creamos nuestro WorkSpace

```bash
mkdir -p ~/jupyter
```

Estamos creando un directorio llamado jupyter dentro de nuestro directorio personal. Con la opcion -p nos permite 
crear los directorios necesarios si todavia no existen y con esto evitamos generar un error si el directorio ya existe

### 4.1 Entramos al directorio

```bash
cd ~/jupyter
```

### 4.2 Corroboramos la version de python

```bash
python --version
```

### 4.3 Creamos un entorno virtual

```bash
python -m venv .venv
```

Estamos creando un entorno virtual de Python llamado .venv dentro de nuestro directorio actual. El objetivo principales
de un entorno virtual es aislar las bibliotecas y dependencias del proyecto de la instalacion global de Python.

### 4.4 Activamos el entorno virtual

```bash
source .venv/bin/activate
```

### 4.5 Actualizamos pip 

```bash
python -m pip install --upgrade pip
```

Estamos actualizando pip, que es el administrador de paquetes de Python, cabe mencionar que estamos usando python 
-m pip en lugar de solo usar pip para asegurarnos de que pip pertenece al Python que estamos ejecutando actualmente,
en este caso, el Python del entorno virtual.

### 4.6 Instalacion de Jupyter Notebook

```bash
python -m pip install notebook
```

Jupyter Notebook nos proporciona la interfaz que permite crear y ejecutar notebooks, normalmente con archivos .ipynb

### 4.7 Instalacion de ipykernel 

```bash
python -m pip install ipykernel
```

ipykernel nos permite utilizar el interprete de Python como un kernel de Jupyter. Recordemos que el kernel es el 
componente que realmente ejecuta el codigo Python que escribimos dentro de un Notebook.

### 4.8 Iniciamos Jupyter Notebook

```bash
jupyter notebook
```

<img width="1475" height="431" alt="image" src="https://github.com/user-attachments/assets/a9976a00-58bc-4829-af61-8acd4540a5a5" />

Si te da el mensaje anterior en la consola es porque el servidor se detuvo inmediatamente, esto debido a que estamos ejecutando 
los comandos en la terminal desde el usuario root, esto causo que Jupyter bloqueara la ejecucion por seguridad y debido a esto no se 
genero la url con el token de seguridad, para solucionar este problema debemos de ejecutar el siguiente comando:

```bash
jupyter notebook --allow-root
```

NOTA: Siempre que estemos en la cuenta root, sera necesario que usemos el comando anterior para iniciar Jupyter Notebook, de lo contraria 
Jupyter bloqueara la ejecucion por seguridad. Si no queremos depender de este comando, bastara con que estemos dentro de una cuenta de usuario
normal, o sea, que no estemos en la cuenta root. Con esto podremos ejecutar el comando jupyter notebook, sin requerir del comando jupyter notebook 
--allow-root.

<img width="1468" height="706" alt="image" src="https://github.com/user-attachments/assets/47037ca4-1cf3-465e-9f1c-f4db0cc53508" />

Con esto ya iniciamos oficialmente el servidor de Jupyter Notebook 

<img width="1917" height="951" alt="image" src="https://github.com/user-attachments/assets/5bfed28e-332c-4764-871c-521c95deef21" />

Para cerrar Jupyter Notebook y que se nos devuelva el control de la terminal, basta con presionar la combinacion de teclas Ctrl + C


