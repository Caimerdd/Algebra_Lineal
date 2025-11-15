print("=== VERIFICANDO IMPORTS ===")
import os

print("Archivos en directorio actual:")
for archivo in os.listdir('.'):
    if archivo.endswith('.py'):
        print(f"  📄 {archivo}")

print("\nIntentando importar Complement.py...")
try:
    from Complement import gauss_steps, resolver_por_cramer
    print("✅ Complement.py importado CORRECTAMENTE")
    
    # Probar una función
    resultado = resolver_por_cramer([[1, 2, 3], [4, 5, 6]])
    print(f"✅ Cramer funciona: {resultado}")
    
except ImportError as e:
    print(f"❌ Error importando Complement.py: {e}")
    
print("\nIntentando importar desde páginas...")
try:
    from paginas.pagina_sistemas_ecuaciones import PaginaSistemasEcuaciones
    print("✅ Páginas importadas CORRECTAMENTE")
except ImportError as e:
    print(f"❌ Error importando páginas: {e}")