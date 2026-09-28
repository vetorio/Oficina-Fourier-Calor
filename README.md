# Simulador Computacional: Equação do Calor

Ferramenta interativa para explorar a **equação do calor 1D** através de
séries de Fourier, com visualização 3D em tempo real e múltiplas
perspectivas animadas.

Desenvolvida no contexto da **Oficina de Física Computacional** da
Universidade Federal de Pernambuco (UFPE).

---

## Visão geral

O simulador resolve numericamente a equação de difusão térmica

$$
\frac{\partial u}{\partial t} = \alpha \, \frac{\partial^2 u}{\partial x^2}
$$

com condições de contorno de Dirichlet e condição inicial uniforme, usando
a solução analítica por separação de variáveis (série de Fourier). Toda a
computação é vetorizada com NumPy; a renderização usa Plotly dentro de um
app Streamlit.

### Funcionalidades

- **Equação interativa** — os termos da solução são editáveis por cartões
  clicáveis, sincronizados com sliders na barra lateral.
- **Duas visualizações 3D:**
  - **Superfície u(x,t)** — a solução completa no espaço-tempo (gráfico
    clássico de EDPs).
  - **Geometria física** — cilindro, barra retangular ou fio fino coloridos
    pela temperatura.
- **Vista única ou mosaico 3×2** — escolha entre seis perspectivas
  predefinidas (Isométrica, Frontal, Lateral, Topo, Traseira, Base),
  visualizadas uma de cada vez ou todas animadas em sincronia.
- **Tema Gruvbox** escuro, tipografia monoespaçada acadêmica.
- **Performance adaptativa** — perfis de qualidade (Econômico, Padrão,
  Alta) que reduzem a resolução em modos mais pesados.

---

## Requisitos

- **Python** ≥ 3.9 (testado em 3.10 e 3.11)
- **pip** ≥ 21
- Navegador moderno com suporte a WebGL2 (Chrome, Edge, Firefox, Safari)
- Sistema operacional: Linux, macOS ou Windows

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/<usuario>/<repositorio>.git
cd <repositorio>
```

### 2. Criar um ambiente virtual

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (cmd):**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

Você saberá que está dentro do venv quando o prompt mostrar `(venv)` no
início da linha.

### 3. Instalar as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Arquivo `requirements.txt`

Crie na raiz do projeto com o seguinte conteúdo:

```txt
streamlit>=1.30,<2.0
numpy>=1.24,<2.0
plotly>=5.18,<6.0
```

### Detalhamento dos pacotes

| Pacote | Versão | Papel |
|---|---|---|
| **streamlit** | ≥ 1.30 | Framework web que serve a UI, gerencia estado e faz o hot-reload do app |
| **numpy** | ≥ 1.24 | Solver vetorizado da série de Fourier e geração das malhas 3D |
| **plotly** | ≥ 5.18 | Renderização interativa 3D (`go.Surface`, `go.Scatter3d`) e animações nativas via `go.Frame` |

Nenhuma dependência adicional é necessária. Streamlit já traz o `tornado`,
`altair` e `pandas` como sub-dependências.

Se você quiser gerar o `requirements.txt` automaticamente a partir do seu
ambiente:

```bash
pip freeze > requirements.txt
```

Mas atenção: esse comando inclui **todas** as dependências transitivas, o
que engessa as versões. Para um projeto pequeno como este, prefira o arquivo
enxuto acima.

---

## Como executar

Com o ambiente virtual ativo e as dependências instaladas:

```bash
streamlit run app_calor.py
```

Substitua `app_calor.py` pelo nome real do seu arquivo principal.

O terminal exibirá algo como:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.10:8501
```

O navegador abrirá automaticamente em `http://localhost:8501`. Se não
abrir, acesse manualmente essa URL.

### Parar o app

`Ctrl + C` no terminal onde o Streamlit está rodando.

### Rodar em porta específica

```bash
streamlit run app_calor.py --server.port 8080
```

### Expor na rede local (para acessar de outro dispositivo)

```bash
streamlit run app_calor.py --server.address 0.0.0.0
```

---

## Guia de uso

### 1. Ajustar parâmetros

Há **dois caminhos equivalentes**, sincronizados em tempo real:

- **Cartões de parâmetro** logo abaixo da equação, na parte superior —
  clique em qualquer termo (`T_L`, `T_R`, `T_init`, `α`, `N`) para expandir
  e digitar um valor.
- **Sliders na barra lateral esquerda**.

| Parâmetro | Significado | Faixa |
|---|---|---|
| `T_L` | Temperatura fixa na borda esquerda (x = 0) | 0 – 100 °C |
| `T_R` | Temperatura fixa na borda direita (x = L) | 0 – 100 °C |
| `T_init` | Temperatura uniforme inicial da barra | 0 – 100 °C |
| `α` | Difusividade térmica | 0.01 – 2.00 |
| `N` | Número de harmônicos de Fourier | 1 – 150 |

### 2. Escolher a visualização

Na sidebar, em **Visualização**:

- **Tipo de gráfico 3D:**
  - *Superfície u(x,t)* — a solução completa no espaço-tempo.
  - *Geometria física colorida* — cilindro / barra / fio coloridos pela
    temperatura.
- **Layout:**
  - *Única vista* — uma cena, câmera controlável pelo mouse.
  - *Mosaico 3×2* — as seis perspectivas simultâneas.

### 3. Animar

Clique em **▶ Play** dentro do próprio gráfico (canto superior esquerdo).
Todas as cenas do mosaico animam em sincronia.

- **Durante o Play**, a câmera fica fixa na vista escolhida.
- Para girar livremente: clique em **⏸ Pause** e arraste sobre o gráfico 3D.
- Scroll do mouse = zoom.

### 4. Ajustar performance

No **mosaico da geometria física** (que renderiza seis superfícies
simultâneas), use o seletor **Qualidade do mosaico**:

| Perfil | Resolução | Máx. frames |
|---|---|---|
| **Econômico** (padrão) | 40 × 8 | 24 |
| **Padrão** | 60 × 12 | 30 |
| **Alta** | 100 × 24 | 60 |

Se a animação travar, use **Econômico** ou reduza o slider de frames.

---

## Estrutura do projeto

```
.
├── app_calor.py          # Aplicação principal (Streamlit + Plotly)
├── requirements.txt      # Dependências Python
├── README.md             # Este arquivo
└── .gitignore            # Exclui venv/, __pycache__/, .streamlit/
```

### `.gitignore` recomendado

```gitignore
# Ambiente virtual
venv/
env/
.venv/

# Cache Python
__pycache__/
*.py[cod]
*.egg-info/

# Streamlit
.streamlit/secrets.toml

# Editores
.vscode/
.idea/
*.swp

# Sistema
.DS_Store
Thumbs.db
```

---

## Solução de problemas

### `streamlit: command not found`

O ambiente virtual não está ativado, ou o Streamlit não foi instalado.
Verifique:

```bash
which streamlit          # Linux/macOS
where streamlit          # Windows
```

Se não retornar caminho dentro de `venv/`, reative o venv e reinstale.

### `ModuleNotFoundError: No module named 'plotly'`

Rode:

```bash
pip install -r requirements.txt
```

Certifique-se de que o venv está ativo antes.

### Animação 3D trava ou fica lenta

1. Reduza a **Qualidade do mosaico** para **Econômico**.
2. Reduza o slider **Nº de frames** para 20.
3. Feche outras abas do navegador que usem WebGL.
4. Teste em Chrome ou Edge em vez de Firefox.

### Erro `ValueError: could not broadcast` no console

Verifique se a versão do código é a mais recente (`git pull`). Esse erro
foi corrigido em versões recentes.

### App abre mas gráfico fica em branco

- Verifique se o JavaScript está habilitado no navegador.
- Tente desabilitar extensões de bloqueio (uBlock, Privacy Badger).
- Abra o console do navegador (F12) e veja se há erros de WebGL.

### Aviso do Streamlit sobre `use_container_width`

A partir do Streamlit 1.40 esse parâmetro foi renomeado. Se você vir um
aviso, atualize a linha:

```python
st.plotly_chart(fig, use_container_width=True)
```

para

```python
st.plotly_chart(fig, width="stretch")
```

---

## Fundamentação matemática

A solução analítica usada no solver é:

$$
u(x,t) = \underbrace{T_L + \frac{x}{L}(T_R - T_L)}_{\text{estado estacionário}}
+ \underbrace{\sum_{n=1}^{N} b_n \sin\!\left(\frac{n\pi x}{L}\right)
e^{-\alpha (n\pi/L)^2 t}}_{\text{transiente de Fourier}}
$$

com coeficientes

$$
b_n = \frac{2}{n\pi} \left[(T_{\text{init}} - T_L)(1 - (-1)^n) + (T_R - T_L)(-1)^n\right]
$$

---

## Licença

Uso acadêmico e educacional. Para uso comercial, consulte os autores.

---

## Referências

- Crank, J. *The Mathematics of Diffusion*. Oxford University Press, 1975.
- Farlow, S. J. *Partial Differential Equations for Scientists and
  Engineers*. Dover, 1993.
- Documentação do Plotly: https://plotly.com/python/
- Documentação do Streamlit: https://docs.streamlit.io/
