package main

import "math"

import "math/rand"
import "math/big"
import "errors"
import "fmt"

type Key struct {
    key int
    n int
}

type KeyPair struct {
    Private Key
    Public Key
}

func isPrime(n int) bool {
    if n == 1 {
        return false
    }


    for i := 2; i <= int(math.Floor(math.Sqrt(float64(n)))); i++ {
        if n % i == 0 {
            return false
        }
    }
    return true
}


func gcd(a int, b int) int {
    for {
      if(a>b){
        a%=b;
      }else{
        b%=a;}
      if (a*b==0){return (a|b);}
    }
  }



func multiplicativeInverse(e int, phi int) int {
    var table [][]int
    A := phi
    B := e
    row := []int{A, B, A % B, A / B, -1, -1}
    table = append(table, row)
    for i := 0; table[i][2] != 0; i++ {
        A = table[i][1]
        B = table[i][2]
        row := []int{A, B, A % B, A / B, -1, -1}
        table = append(table, row)
    }

    table[len(table)-1][4] = 0
    table[len(table)-1][5] = 1
    for i := len(table)-2; i >= 0; i-- {
        table[i][4] = table[i+1][5]
        table[i][5] = table[i+1][4] - table[i+1][5]*table[i][3]
    }

    r := table[0][5] % phi
    if r < 0 {
        r = r + phi
    }
    return r
}


func GenerateKeypair(p int, q int) (KeyPair, error) {
    if !(isPrime(p) && isPrime(q)){
        return KeyPair{}, errors.New("Both numbers must be prime.")
    } else if  p == q {
        return KeyPair{}, errors.New("p and q can't be equal.");
    }

    n := p * q
    phi := (p - 1)*(q - 1)
    e := rand.Intn(phi - 1) + 1
    g := gcd(e, phi)
    for g != 1 {
        e = rand.Intn(phi - 1) + 1
        g = gcd(e, phi)
    }

    d := multiplicativeInverse(e, phi)
    return KeyPair{Key{e, n}, Key{d, n}}, nil
}


func Encrypt(pk Key, plaintext string) []int {
    cipher := []int{}
    n := new(big.Int)
    for _, ch := range plaintext {
        n = new(big.Int).Exp(
            big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
        n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
        cipher = append(cipher, int(n.Int64()))
    }
    return cipher
}


func Decrypt(pk Key, cipher []int) string {
    plaintext := ""
    n := new(big.Int)
    for _, ch := range cipher {
        n = new(big.Int).Exp(
            big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
        n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
        plaintext += string(rune(int(n.Int64())))
    }
    return plaintext
}
func main(){
  var q, p int;

  fmt.Print("Enter a number: ")
  fmt.Scan(&q)
  fmt.Print("Enter another number: ")
  fmt.Scan(&p)
  //var pk KeyPair
  pk, _:= GenerateKeypair(p,q)
  var text string
  fmt.Scan(&text)
  var encrypted []int
  encrypted = Encrypt(pk.Private,text)
  var decrypted string
  decrypted = Decrypt(pk.Public, encrypted)
  fmt.Println(encrypted)
  fmt.Println(decrypted)

}
