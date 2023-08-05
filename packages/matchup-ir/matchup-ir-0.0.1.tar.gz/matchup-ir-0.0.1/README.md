# MatchUp

Atualmente, por meio de máquinas de busca, é comum realizar consultas que apresentam, como resultado, um número elevado de referências que não atendem aos contextos das mesmas. Com o propósito de proporcionar resultados relevantes, mediante consultas, alguns modelos da área de Recuperação de Informação, chamados clássicos, foram propostos: o Booleano, o Vetorial e o Probabilístico. Por sua vez, visando a melhoria da qualidade dos resultados gerados pela aplicação dos modelos clássicos de Recuperação de Informação, foram definidos, a partir dos mesmos, modelos estendidos de Recuperação de Informação; dentre eles, tem-se o Extended Boolean, o Generalized Vector e o Belief Network. 
 
Em 2018/1, foi desenvolvida a primeira versão da ferramenta MatchUp: uma ferramenta Web para cálculo de similaridade entre uma consulta, podendo ser um determinado documento ou um conjunto de termos de interesse do usuário, e uma coleção de documentos, possibilitando a geração de uma lista de documentos desta coleção que são relevantes à consulta desejada. Para cálculo de similaridade, tal versão contemplou os modelos clássicos de RI e o modelo estendido Extended Boolean. Por meio da análise dos resultados dos experimentos realizados, foi possível perceber que o modelo Vetorial, de uma forma geral, apresentou os melhores resultados quando comparado aos demais modelos implementados. Porém, a MatchUp não contemplou os modelos estendidos Generalized Vector e Belief Network, que podem apresentar melhores resultados que o Modelo Vetorial. Logo, este projeto de iniciação científica possui, como objetivo principal, o desenvolvimento da versão 2.0 da ferramenta MatchUp, no intuito de contemplar também os modelos estendidos Generalized Vector e Belief Network. Para validar a versão 2.0 da ferramenta MatchUp, experimentos serão realizados, envolvendo distintas coleções de documentos. 
 
 

## Objetivos

Este projeto de iniciação científica possui, como objetivo principal, o desenvolvimento da versão 2.0 da ferramenta MatchUp, no intuito de contemplar os modelos estendidos Generalized Vector e Belief Network de RI. A MatchUp consiste em uma ferramenta Web para cálculo de similaridade entre uma consulta, podendo ser um determinado documento ou um conjunto de termos de interesse do usuário, e uma coleção de documentos, possibilitando a geração de uma lista de documentos desta coleção que são relevantes à consulta desejada. Para cálculo de similaridade, a versão 1.0 da MatchUp contemplou os modelos clássicos de RI e o modelo estendido Extended Boolean. 
 
Os objetivos específicos a serem atingidos são:
- implementação de distintos modelos estendidos de RI;
- definição de uma interface amigável para a ferramenta Web, de forma a facilitar a entrada dos dados necessários para a execução da mesma e permitir a intervenção do usuário, se for de interesse, na definição de características de funcionalidade quanto aos modelos de RI implementados;
- realização de experimentos de validação da ferramenta Web desenvolvida, por meio da execução da mesma para distintas coleções de documentos;
- estudo comparativo da eficácia dos modelos de RI implementados, com base nos resultados experimentais obtidos;
- levantamento de dados estatísticos quanto aos termos presentes em uma determinada coleção de documentos;
- capacitação do bolsista do projeto, preparando-o para cursar um programa de pósgraduação e, consequentemente, minimizando o seu tempo de permanência em tal programa;
- consolidação da linha de pesquisa Tratamento e Recuperação da Informação do Departamento de Computação da Universidade Federal de Ouro Preto. 

## Tecnologias 
* [Python 3.7](https://www.python.org/) - Linguagem de Programação

## STATUS : Em construção
