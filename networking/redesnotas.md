\## ICMP



Objetivo: Capturar e analisar pacotes ICMP gerados pelos comandos `ping` e `tracert` no Wireshark para entender a estrutura dos pacotes e o funcionamento do protocolo ICMP e do campo TTL (Time To Live).



\- `ping 8.8.8.8`: envia requisições ICMP Echo Request para um destino para testar a conectividade

\- `tracert google.com`: mapeia a rota até o destino enviando pacotes ICMP com TTL crescente

\- `icmp`: filtro aplicado no Wireshark para exibir apenas o tráfego do protocolo ICMP



O que deu errado: fiquei com dúvida no funcionamento do `tracert` e no motivo pelo qual o TTL aumenta progressivamente a cada pacote enviado, além de ter esquecido de registrar o print inicial.



O que aprendi:

\- O `ping` envia requisições ICMP Echo Request (Tipo 8) e recebe respostas ICMP Echo Reply (Tipo 0). No Windows, o tamanho padrão do payload é de 32 bytes e o valor inicial do TTL é 128.

\- O TTL (Time To Live) limita a quantidade de saltos (roteadores) que um pacote pode dar antes de ser descartado, evitando loops infinitos na rede.

\- O `tracert` incrementa o TTL sequencialmente (1, 2, 3...) para forçar que cada roteador no caminho descarte o pacote quando o TTL chegar a 0 e responda com uma mensagem ICMP \*Time-to-live exceeded\* (Tipo 11), permitindo mapear todos os roteadores do caminho até o destino final.

