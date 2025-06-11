<header>A Smart Farofoto 3x4 automatiza processos manuais na produção e impressão de fotografias 3x4cm através de poucos cliques. O software pode ser acessado pelo menu de contexto do Windows, quando apertamos com o botão direito sobre um arquivo e escolhemos alguma opção. O sistema foi desenvolvido utilizando a linguagem Python com o utilitário OpenCV e Tkinker e classificadores em cascata para detecção de faces. A automação trouxe benefícios ao cotidiano do comércio Loja Farofoto, onde aumentou a eficiência ao tempo de atendimento aos clientes, eliminação de procedimentos manuais pelos funcionários e o menor desgaste de equipamentos eletrônicos removíveis como cartões de memória. <br>
	<br>
	<br>
</header> 	

<t1><b>SETUP PARA BAIXAR E INSTALAR O SMART FAROFOTO 3X4 (utilizando o menu de contexto do Windows)</b></t1>

1. Baixar ou já ter instalado Python 3.x (de preferência uma versão mais recente).
	- Para verificar se já há o Python instalado na máquina pode utilizar o comando "where python" no prompt de comando do Windows. Isso irá retornar o caminho absoluto da instalação já realizada do Python, se existir.
	- Caso não tenha instalado, consequentemente, não apareceu o local de instalação do Python da instrução anterior, baixe através desse link: <https://www.python.org/downloads/>. Apenas clique no botão amarelo redondo "Download Python (versão...)". Após baixar o instalador, clique sobre o programa e efetue a instalação padrão.

2. Baixar o ZIP do projeto Smart Farofoto 3x4 no GitHub e extrair para o local indicado
   
	- Acesse o link: <https://github.com/joaolbasso/SmartFarofoto3x4>;
	- No botão verde arredondado com a escrita "Code", clique sobre ele e selecione a opção "Download ZIP";
	- O navegador irá iniciar o download e descarregar na pasta padrão, muito provavelmente de "Downloads";
	- Dentro do explorador de arquivos, encontre o arquivo SmartFarofoto3x4-main.zip;
	- Clique com o botão direito sobre ele e clique em "Extrair Tudo" e na janela seguinte "Extrair".
	- Selecione a pasta e extraia esse diretório com "CTRL + X" ou com o botão direito do mouse sobre a pasta selecionando a opção "RECORTAR";
	- Vá para "Este Computador" então para "Disco Local (C:)" e cole o arquivo recortado, pressione "CTRL + V" ou, clique com o botão direito do mouse, e "COLAR". (O local do arquivo é crucial para o funcionamento da aplicação, pois no próximo passo, o editor de registros precisa exatamente do local correto da aplicação dentro de seu computador).

3. Executando o Editor de Registros do Windows
   
	- Abra a pasta "SmartFarofoto3x4-main", após isso abra a pasta "SmartFarofoto3x4-main" (isso acontece devido à extração do passo anterior);
	- Clique sobre o arquivo "EditorDeRegistroComExecutavel" e confirme todas as operações, "Executar" -> "Sim" -> "Sim".

	===== ATENÇÃO!!!!! =====
	ESSA ETAPA É CRUCIAL PARA O FUNCIONAMENTO DA APLICAÇÃO NO MENU DE CONTEXTO DO WINDOWS. Se você extraiu e colou o diretório em outro pasta ou alterou o nome dos arquivos, essa etapa apresentará falhas. Esse arquivo de edição de registros está preparado para executar o código diretamente no "Disco Local (C:)" e com os nomes que foram extraídos do GitHub.

4. Testando a aplicação
   
	- Clique com o botão direito sobre um arquivo de imagem, (selecione "Mostrar Mais Opções" (Windows 11)), então aparecerá a opção "Gerar Fotos 3x4cm Farofoto", clique nela e o software será executado. A sua foto recortada aparecerá dentro do mesmo local em que o arquivo selecionado está, dentro de uma pasta chamada "Farofoto_Output"

 5. **Se a aplicação der um erro do tipo "Não há aplicativo padrão para essa tarefa":
	- Procure um arquivo de imagem, clique com o botão direito sobre ele e vá até "ABRIR COM";<br>
	- Dentro do menu "ABRIR COM", selecione "ESCOLHER OUTRO APLICATIVO", aparecerá uma lista com vários aplicativos;<br>
	- Selecione o aplicativo de sua preferência e assinale a caixa de relacionamento que aparece ao fim da janela com uma mensagem do tipo "Sempre abrir com esse aplicativo...";<br>
	- Retorne ao passo 4 e teste novamente a aplicação .<br>
	- Se o erro persistir é provável que houve falha na edição de registro do Windows do passo 3. Revise os caminhos e nomes dos arquivos. Se quiser e preferir, pode alterar o arquivo "EditorDeRegistroComExecutavel" com o caminho absoluto de onde sua aplicação está localizada.<br>
<br><br>
Aproveite a aplicação! :)
