# APIClientDatabricks
#Clonar o repositório
git clone https://github.com/williamfp7/APIClientDatabricks.git

#Entrar na pasta
cd APIClientDatabricks

#Definir variáveis de ambiente
#Atenção!!! O Databricks Instance deve ser do https:// até o .net!
export SICRM_API=<Databricks Instance>
export SICRM_Token=<Token>
export SICRM_Secret_Scope=<Secret Scope>

#Criando os jobs
python3 main.py SICRM_Chave_Cliente /Shared/SICRM/CI/Cadastro/Visao_Chave_Cliente
python3 main.py SICRM_Cadastro_Cliente /Shared/SICRM/CI/Cadastro/Visao_Cadastro_Cliente
python3 main.py SICRM_Cliente_COCLI /Shared/SICRM/CI/Cadastro/Visao_Cliente_COCLI
python3 main.py SICRM_Cliente_Nicho /Shared/SICRM/CI/Cadastro/Visao_Cliente_Nicho
python3 main.py SICRM_Cliente_Vinculo /Shared/SICRM/CI/Cadastro/Visao_Cliente_Vinculo
