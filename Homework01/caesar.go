package main
import "fmt"
func isLetter(c rune) bool {
    return ('a' <= c && c <= 'z') || ('A' <= c && c <= 'Z')
}
func EncryptCaesar(plaintext string, shift int) string {
    var ciphertext string
    shift %= 26
    for _, ch := range plaintext {
        if (isLetter(rune(ch))) {
            if (ch + rune(shift) > 'Z' && ch <= 'Z') ||
               (ch + rune(shift) > 'z') {
                ch -= 26
            }
            ciphertext += string(ch + rune(shift))
        } else {
            ciphertext += string(ch)
        }
    }

    return ciphertext
}


func DecryptCaesar(ciphertext string, shift int) string {
    var plaintext string

    shift %=  26
    for _, ch := range ciphertext {
        if (isLetter(rune(ch))) {
            if (ch - rune(shift) < 'A' && ch >= 'A') ||
               (ch - rune(shift) < 'a' && ch >= 'a') {
                ch += 26
            }
            plaintext += string(ch - rune(shift))
        } else {
            plaintext += string(ch)
        }
    }

    return plaintext
}
func main(){
  fmt.Println(EncryptCaesar("python", 3));
}
