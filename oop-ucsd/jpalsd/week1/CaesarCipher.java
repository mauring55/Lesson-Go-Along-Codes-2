package jpalsd.week1;

public class CaesarCipher {
    public String encrypt(String input, int key) {
        String output = "";
        String alphabet = "abcdefghijklmnopqrstuvwxyz";
        String cryptographicKey = alphabet.substring(key) + alphabet.substring(0,key);
        for (int i = 0; i < input.length(); i++) {
            char currChar = input.charAt(i);
            char shiftedChar = currChar;
            if (Character.isLetter(currChar)) {
                int indexCurrChar = alphabet.indexOf(Character.toLowerCase(currChar));
                shiftedChar = cryptographicKey.charAt(indexCurrChar);
            }
            if (Character.isUpperCase(currChar)) {
                output += Character.toUpperCase(shiftedChar);
            }
            else {
                output += shiftedChar;
            }
        }
        return output;
    }
    public String encryptTwoKeys(String input, int key1, int key2) {
        String output = "";
        String oddChars = "";
        String evenChars = "";

        for (int i = 0; i < input.length(); i++) {
            if ((i+1) % 2 == 0) {
                evenChars += input.charAt(i);
            }
            else {
                oddChars += input.charAt(i);
            }
        }
        String encryptedOddChars = encrypt(oddChars, key1);
        String encryptedEvenChars = encrypt(evenChars, key2);

        for (int i = 0; i< input.length(); i++) {
            if ((i+1) % 2 == 0) {
                output += encryptedEvenChars.charAt(0);
                encryptedEvenChars = encryptedEvenChars.substring(1);
            }
            else {
                output += encryptedOddChars.charAt(0);
                encryptedOddChars = encryptedOddChars.substring(1);
            }
        }
        return output;
    }
    public void testEncrypt() {
        String[] inputArr1 = {"FIRST LEGION ATTACK EAST FLANK!",
                              "eeeeeeeeeeeeeeeees",
                              "First Legion",
                              "First Legion",
                              "At noon be in the conference room with your hat on for a surprise party. YELL LOUD!"};
        Integer[] inputArr2 = {23,2,23,17,15};
        String[] outputArr = {"CFOPQ IBDFLK XQQXZH BXPQ CIXKH!",
                              "gggggggggggggggggu",
                              "Cfopq Ibdflk",
                              "Wzijk Cvxzfe",
                              "Pi cddc qt xc iwt rdcutgtcrt gddb lxiw ndjg wpi dc udg p hjgegxht epgin. NTAA ADJS!"};

        for (int i = 0; i < inputArr1.length; i++) {
            String currInput1 = inputArr1[i];
            int currInput2 = inputArr2[i];
            String answer = outputArr[i];
            String currResult = encrypt(currInput1, currInput2);
            if (!currResult.equals(answer)) { 
                System.out.println(String.format("Test %d - Failed", i+1));
                System.out.println(String.format("Result should be: %s", answer));
                System.out.println(String.format("Instead got: %s", currResult));
            }
        }
        System.out.println("encrypt Tests Completed");
    }
    public void testEncryptTwoKeys() {
        String[] inputArr1 = {"First Legion",
                              "AbAbAb",
                              "At noon be in the conference room with your hat on for a surprise party. YELL LOUD!",
                              "Gwpv c vbuq pvokki yfve iqqu qc bgbgbgbgbgbgbgbgbu",
                              "Top ncmy qkff vi vguv vbg ycpx"};
        Integer[] inputArr2 = {23,1,8,26-23,26-(4-2)};
        Integer[] inputArr3 = {17,2,21,26-(4-2),26-20};
        String[] outputArr = {"Czojq Ivdzle",
                              "BdBdBd",
                              "Io iwjv jz dv bcm kjvammmikz mwju edbc twpz pvb wi awm v ncmxmqnm xvzog. TMGT TJCY!",
                              "Just a test string with lots of eeeeeeeeeeeeeeeees",
                              "Run like wild to beat the wind"};
        
        for (int i = 0; i <  inputArr1.length; i++) {
            String currInput1 = inputArr1[i];
            int currInput2 = inputArr2[i];
            int currInput3 = inputArr3[i];
            String answer = outputArr[i];
            String currResult = encryptTwoKeys(currInput1, currInput2,currInput3);
            if (!currResult.equals(answer)) { 
                System.out.println(String.format("Test %d - Failed", i+1));
                System.out.println(String.format("Result should be: %s", answer));
                System.out.println(String.format("Instead got: %s", currResult));
            }
        }
        System.out.println("encryptTwoKeys Tests Completed");
    }
    public static void main(String[] args) {
        CaesarCipher c = new CaesarCipher();
        c.testEncrypt();
        c.testEncryptTwoKeys();
    }
}
