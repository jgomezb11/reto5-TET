# Reto 5
>Este repositorio es el producto de mi trabajo para familiarizarme con el paradigma de MapReduce, un modelo de programación eficiente para procesar grandes volúmenes de datos en paralelo. MapReduce es particularmente útil para las tareas de procesamiento de datos en la era del Big Data.

## Información de la asignatura
---

 -  **Nombre de la asignatura:** Tópicos especiales en telemática.
-   **Código de la asignatura:**  C2361-ST0263-4528
-   **Departamento:** Departamento de Informática y Sistemas (Universidad EAFIT).
-   **Nombre del profesor:** Juan Carlos Montoya Mendoza.
-  **Correo electrónico del docente:** __[jcmontoy@eafit.edu.co](mailto:jcmontoy@eafit.edu.co)__.

## Datos del estudiante
---

-   **Nombre del estudiante:** Julian Gámez Benítez.
-  **Correo electrónico del estudiante:** __[jgomezb11@eafit.edu.co](mailto:jgomezb11@eafit.edu.co)__.

## Descripción y alcance del proyecto
---
En este proyecto, utilizo la biblioteca Python MRJob, que simplifica la escritura, prueba y ejecución de aplicaciones MapReduce. MRJob es compatible con varias plataformas para ejecutar trabajos de MapReduce, incluyendo la ejecución en local para el desarrollo y la depuración, y la ejecución en plataformas como Hadoop o Amazon EMR para el procesamiento a gran escala.
El proyecto consiste en una serie de scripts de Python que implementan trabajos MapReduce para analizar un conjunto de datos. Cada script demuestra una capacidad específica de MapReduce y MRJob, desde tareas simples de conteo hasta cálculos más complejos de clasificación y agregación.


## Paso a paso del desarrollo
---

### 1. Creacion y conexion al cluster EMR.

Comenzamos configurando las credenciales de AWS para acceder a los servicios:

-   Abrimos el archivo `~/.aws/credentials` y agregamos lo siguiente:
```
[default]
aws_access_key_id = SECRET_ACCES_KEY
aws_secret_access_key = SECRET_KEY
aws_session_token = SECRET_KEY
```
A continuación, descargamos e instalamos la AWS CLI en Windows y asegúrate de configurar las variables de entorno correctamente.

Creamos un bucket en Amazon S3 con el siguiente comando:

```bash
aws s3 mb s3://bucket-reto5-julian
```

Ahora, creamos las carpetas necesarias en el bucket de S3:
```bash
aws s3api put-object --bucket bucket-reto5-julian --key logs/
aws s3api put-object --bucket bucket-reto5-julian --key inputs/
aws s3api put-object --bucket bucket-reto5-julian --key outputs/
aws s3api put-object --bucket bucket-reto5-julian --key scripts/
```

![bucket](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/creacion_bucket.png)

Creamos un security group:

![sg](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/creacion_sg.png)

Le creamos un ingress de la siguiente forma:

```bash
aws ec2 authorize-security-group-ingress --group-id sg-0aa30d7338ae4a7ba --protocol tcp --port 22 --cidr 0.0.0.0/0
```

![ingress](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/ingress_rule.png)

Ahora si podemos crear el cluster EMR haciendo uso de todo lo que hemos creado previamente:

```bash
aws emr create-cluster --name reto5-julian-cluster --applications Name=Hadoop Name=Hive \
--release-label emr-5.33.0 --use-default-roles \
--instance-count 3 --instance-type m4.large \
--ebs-root-volume-size 12 \
--log-uri s3://bucket-reto5-julian/logs \
--ec2-attributes KeyName=reto5,AdditionalMasterSecurityGroups=sg-0aa30d7338ae4a7ba \
--no-auto-terminate
```

![cluster](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/create_cluster.png)

Describimos el cluster para obtener su DNS publico:

```bash
aws emr describe-cluster --cluster-id j-27XWRJEY65MXD
```

![desc](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/describe_cluster.py.png)

Teniendo el DNS nos podemos conectar por medio de SSH:

```bash
ssh hadoop@ec2-34-201-71-133.compute-1.amazonaws.com -i MasterKey.pem
```
### 2. Configuracion del EMR

Lo primero que vamos a hacer es clonar el repositorio del curso:

```bash
sudo git clone https://github.com/ST0263/st0263-2023-1.git
```

Luego vamos a instalar las dependencias necesarias para ejecutar los programas de prueba que tenemos

```bash
sudo yum install git python3-pip && sudo pip3 install mrjob
```

Una vez teniendo eso podemos explorar los ejemplos que se proporcionan, moviendonos a la carpeta del reto 6 y ejecutando los scripts que alli se encuentran:

```bash
cd st0263-2023-1/Laboratorio\ N6-MapReduce/wordcount/
```

y para ejecutar los ejemplos:

```bash
sudo python wordcount-local.py ../../datasets/gutenberg-small/*.txt
```

o

```bash
python wordcount-mr.py ../../datasets/gutenberg-small/*.txt
```

En una parte del reto se propone ejecutar el EMR con archivos que se encuentren en s3... Se subio la carpeta de datasets al s3 bucket que habiamos creado previamente:

![s3](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/upload_s3.py.png)

Luego se ejecuto el siguiente comando:

```bash
python wordcount-mr.py -r emr s3://bucket-reto5-julian/inputs/datasets/gutenberg-small/*.txt --output-dir s3://bucket-reto5-julian/outputs/results/ -D mapred.reduce.tasks=10
```

Pero por un problema de permisos de IAM no se puedo verificar la ejecucion total del comando:

![error](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/error_iam_cred.py.png)


### 3. Retos de programacion usando Map Reduce

En esta seccion se presenta el numero del reto, como se corre y el resultado que dio la implementacion que se encuentra en cada una de las carpetas correspondientes.

#### Reto 1

 1. Literal 1: 
	 `python average_se.py ../../st0263-2023-1/datasets/otros/dataempleados.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto1-lit1.png)
2. Literal 2:
 `python average_employee.py ../../st0263-2023-1/datasets/otros/dataempleados.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto1-lit2.png)
3. Literal 3:
`python se_employee.py ../../st0263-2023-1/datasets/otros/dataempleados.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto1-lit3.png)

#### Reto 2

 1. Literal 1: 
 `python min_day-max_day.py ../../st0263-2023-1/datasets/otros/dataempresas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto2-lit.png)
2. Literal 2:
`python crescent_actions.py ../../st0263-2023-1/datasets/otros/dataempresas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto2-lit2.png)
3. Literal 3:
`python black_day.py ../../st0263-2023-1/datasets/otros/dataempresas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto2-lit3.png)

#### Reto 3

 1. Literal 1: 
 `python UserMovies.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto3-lit1.png)
2. Literal 2:
`python MostMoviesDay.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto3-lit2.png)
3. Literal 3:
`python LeastMoviesDay.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto3-lit3.png)
4. Literal 4:
`python UsersSameMovie.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto3-lit4.png)
5. Literal 5:
`python WorstDay.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto3-lit5.png)
6. Literal 6:
`python BestDay.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto3-lit6.png)
7. Literal 7:
`python WorstBestGender.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt`
	 ![](https://raw.githubusercontent.com/jgomezb11/reto5-TET/main/static/reto3-lit7.png)


## Referencias

[CLI Installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
[EMR Cluster creation]("https://thecodinginterface.com/blog/create-aws-emr-with-aws-cli/")
