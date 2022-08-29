# APIClientDatabricks
#Clonar o repositório<br/>
git clone https://github.com/williamfp7/APIClientDatabricks.git<br/>
<br/>
#Entrar na pasta<br/>
cd APIClientDatabricks<br/>
<br/>
#Editar o arquivo sicrm.json variáveis de acesso<br/>
#Atenção!!! O Databricks Instance deve ser do https:// até o .net!<br/>
<pre>
{
    "URI":"&lt;DATABRICKS URI&gt;",
    "Token":{
        "value":"&lt;TOKEN&gt;"
    },
    "proxies":{"http":"&lt;PROXY&gt;"}
}
</pre>
<br/>

#Criptografar o arquivo sicrm.json para criar o sicrm.ini
python3 encryptToken.py &lt;SENHA&gt;<br/>
<br/>
#Criando os jobs<br/>
python3 createIfNotExists.py &lt;SENHA&gt; &lt;JOB NAME&gt; &lt;NOTEBOOK PATH&gt; &lt;SECRET SCOPE&gt;<br/>
<br/>
#Executando os Jobs<br/>
python3 execute.py &lt;SENHA&gt; &lt;JOB NAME&gt;<br/>