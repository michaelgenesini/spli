cripted = fopen("~/spli/05\ CESARE/files/frequency_crypted.txt","r","native");
statistics = fopen("frequenze_en","r","native");

format1='%f';
format2='%s';

%C: Lettere del testo cifrato
C=fscanf(cripted,format2,1);
C

%S: Lettere della statistica
S=fscanf(statistics,format2,1);
S


%OC: Occorrenze lettere del testo cifrato
OC=fscanf(cripted,format1,26);
OC;

%OS: Occorrenze lettere della statistica
OS=fscanf(statistics,format1,26);
OS;

%Numero lettere alfabeto
x = 1:26;

figure;

%Primo Plot: Grafico della statistica
p1 = subplot(2,1,1)
plot(x, OS, 'b')
title('Letter Frequency');
xlabel('Letters'); 
ylabel('Occurrences %'); 
grid; 
set(gca, 'XTick',1:26, 'XTickLabel',{S(1) S(2) S(3) S(4) S(5) S(6) S(7) S(8) S(9) S(10) S(11) S(12) S(13) S(14) S(15) S(16) S(17) S(18) S(19) S(20) S(21) S(22) S(23) S(24) S(25) S(26)})



%Secondo Plot: Grafico del Criptato
p2 = subplot(2,1,2)
plot(x, OC, 'r')
title('Caesar Cipher Attack');
xlabel('Letters'); 
ylabel('Occurrences %'); 
grid; 
set(gca, 'XTick',1:26, 'XTickLabel',{C(1) C(2) C(3) C(4) C(5) C(6) C(7) C(8) C(9) C(10) C(11) C(12) C(13) C(14) C(15) C(16) C(17) C(18) C(19) C(20) C(21) C(22) C(23) C(24) C(25) C(26)})

%Purtroppo non funziona su osx ma solo su linux
%print -djpg Graph.jpg


fclose(cripted);
fclose(statistics);
