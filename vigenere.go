package main
import "fmt"
import "strings"
import "unicode/utf8"
func isLetter(c rune) bool {
    return ('a' <= c && c <= 'z') || ('A' <= c && c <= 'Z')
}
func Fast_Encode(a, b rune) rune {
	return (((a - 'A') + (b - 'A')) % 26) + 'A'
}

func Fast_Decode(a, b rune) rune {
	return (((((a - 'A') - (b - 'A')) + 26) % 26) + 'A')
}
func To_Upper(input string) string{
  output := []rune{}
	for _, v := range input {
    if(!isLetter(v)){
      output = append(output,v)
    }
		if 65 <= v && v <= 90 {
			output = append(output, v)
		} else if 97 <= v && v <= 122 {
			output = append(output, v-32)
		}
	}

	return string(output)
}

func encrypt_vigenere(plaintext string, shift string) string{
  var nshift, ntext string
  nshift, ntext = To_Upper(shift), To_Upper(plaintext)
  var  key_string string
  out := make([]rune, 0, len(ntext))
  key_string = strings.Repeat(nshift, utf8.RuneCountInString(ntext))
  for i, ch := range ntext {

      out = append(out, Fast_Encode(ch, rune(  key_string[i])))
  }
  return string(out)
}
func decrypt_vigenere(ciphertext, key string) string {
  var smsg, skey string
	smsg, skey = To_Upper(ciphertext), To_Upper(key)
  var  key_string string
	out := make([]rune, 0, len(ciphertext))
  key_string = strings.Repeat(skey, utf8.RuneCountInString(smsg))
	for i, ch := range smsg {
		out = append(out, Fast_Decode(ch, rune(  key_string[i])))
	}
	return string(out)
}
func main(){
  var str string
  str = encrypt_vigenere("ATTACKATDAWN", "LEMON")
  fmt.Println(str)
  fmt.Println(decrypt_vigenere(str, "LEMON"))
}
