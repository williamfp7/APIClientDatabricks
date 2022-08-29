# APIClientDatabricks
#Clonar o repositório<br/>
git clone https://github.com/williamfp7/APIClientDatabricks.git<br/>
<br/>
#Entrar na pasta<br/>
cd APIClientDatabricks<br/>
<br/>
#Editar o arquivo sicrm.json variáveis de acesso<br/>
#Atenção!!! O Databricks Instance deve ser do https:// até o .net!<br/>
{
    "URI":"<DATABRICKS URI>",
    "Token":{
        "value":"<TOKEN>"
    },
    "proxies":{"http":"<PROXY>"}
}
<br/>

#Criptografar o arquivo sicrm.json para criar o sicrm.ini
python3 encryptToken.py <SENHA><br/>
<br/>
#Criando os jobs<br/>
python3 createIfNotExists.py <SENHA> <JOB NAME> <NOTEBOOK PATH> <SECRET SCOPE><br/>
<br/>
#Executando os Jobs<br/>
python3 execute.py <SENHA> <JOB NAME><br/>