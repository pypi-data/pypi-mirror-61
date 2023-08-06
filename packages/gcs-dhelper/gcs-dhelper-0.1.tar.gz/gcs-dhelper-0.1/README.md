# gcs-dhelper
gcs-dhelper es una biblioteca hecha para facilitar el uso de Google Cloud Storage en python permitiendo crear clientes y buckets de forma sencilla.

# Antes de usar:
Esta biblioteca se autentica con una service account la cual se descarga en formato json desde "services accounts" de la seccion IAM & admin de Google Cloud Storage.

# Como usar:
Para **crear un cliente** se debe como seguir este codigo de ejemplo:
```python
cliente = GCSClientBuilder() \
    .with_service_account('Credentials.json') \
    .build()
```
donde *'Credentials.json'* es la direccion donde se encuentran sus credenciales.

Para **crear un bucket** se deberan especificar tanto que cliente usar y el bucket en cuestion:

```python
  bucket = GCSBucketBuilder()\
    .with_service_account('Credentials.json')\
    .with_bucket_name('bucket')\
    .build()
```
  Donde cliente es el cliente deseado y previamente creado con *GCSClientBuilder* y *'bucket'* es el nombre del bucket deseado.