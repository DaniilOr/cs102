package main
import "fmt"
import "strings"
import "unicode/utf8"
func isLetter(c rune) bool {
    return ('a' <= c && c <= 'z') || ('A' <= c && c <= 'Z')
}
func Fast_Encode_Upper(a, b rune) rune {
	return (((a - 'A') + (b - 'A')) % 26) + 'A'
}

func Fast_Decode_Upper(a, b rune) rune {
	return (((((a - 'A') - (b - 'A')) + 26) % 26) + 'A')
}
func Fast_Encode_Lower(a, b rune) rune {
	return (((a - 'a') + (b - 'a')) % 26) + 'a'
}

func Fast_Decode_Lower(a, b rune) rune {
	return (((((a - 'a') - (b - 'a')) + 26) % 26) + 'a')
}


func encrypt_vigenere(plaintext string, shift string) string{

  var  key_string string
  out := make([]rune, 0, len(plaintext))
  key_string = strings.Repeat(shift, utf8.RuneCountInString(plaintext))
  for i, ch := range plaintext {
      if !isLetter(rune(plaintext[i])) {
        out = append(out,rune(plaintext[i]))
      } else if rune(plaintext[i])>='a' && rune(plaintext[i])<='z'{
      out = append(out, Fast_Encode_Lower(ch, rune(key_string[i])))
  } else{
    out = append(out, Fast_Encode_Upper(ch, rune(key_string[i])))
  }
}
  return string(out)
}
func decrypt_vigenere(ciphertext, key string) string {
  var  key_string string
	out := make([]rune, 0, len(ciphertext))
  key_string = strings.Repeat(key, utf8.RuneCountInString(ciphertext))
  for i, ch := range ciphertext {
      if !isLetter(rune(ciphertext[i])) {
        out = append(out,rune(ciphertext[i]))
      } else if rune(ciphertext[i])>='a' && rune(ciphertext[i])<='z'{
      out = append(out, Fast_Decode_Lower(ch, rune(  key_string[i])))
  } else{
    out = append(out, Fast_Decode_Upper(ch, rune(key_string[i])))
  }
}
	return string(out)
}
func main(){
  var str string
  str = encrypt_vigenere("python3.5", "a")
  fmt.Println(str)
  fmt.Println(decrypt_vigenere(str, "a"))
}
