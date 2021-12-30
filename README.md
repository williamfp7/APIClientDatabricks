# APIClientDatabricks
#Clonar o repositório<br/>
git clone https://github.com/williamfp7/APIClientDatabricks.git<br/>
<br/>
#Entrar na pasta<br/>
cd APIClientDatabricks<br/>
<br/>
#Definir variáveis de ambiente<br/>
#Atenção!!! O Databricks Instance deve ser do https:// até o .net!<br/>
export SICRM_API=&#060;<Databricks Instance&#062;<br/>
export SICRM_Token=&#060;Token&#062;<br/>
export SICRM_Secret_Scope=&#060;Secret Scope&#062;<br/>
<br/>
#Criando os jobs<br/>
python3 main.py SICRM_Chave_Cliente /Shared/SICRM/CI/Cadastro/Visao_Chave_Cliente<br/>
python3 main.py SICRM_Cadastro_Cliente /Shared/SICRM/CI/Cadastro/Visao_Cadastro_Cliente<br/>
python3 main.py SICRM_Cliente_COCLI /Shared/SICRM/CI/Cadastro/Visao_Cliente_COCLI<br/>
python3 main.py SICRM_Cliente_Nicho /Shared/SICRM/CI/Cadastro/Visao_Cliente_Nicho<br/>
python3 main.py SICRM_Cliente_Vinculo /Shared/SICRM/CI/Cadastro/Visao_Cliente_Vinculo<br/>
