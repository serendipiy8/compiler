import ply.lex as lex
import define

data = '''
int main() {
    int x = 10;
    float y=10.21;
}
'''

define.lexer.input(data)

for token in define.lexer:
    print(token)