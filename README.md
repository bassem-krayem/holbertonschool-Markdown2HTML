# holbertonschool-Markdown2HTML

in this ripo we will make a python script that convert marcdown language to html

## Description

Markdown is awesome! All your README.md are made in Markdown, but do you know how GitHub are rendering them?

## Requirements

- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7 or higher)
- The first line of all your files should be exactly #!/usr/bin/python3
- A README.md file, at the root of the folder of the project, is mandatory
- Your code should use the PEP 8 style (version 1.7.\*)
- All your files must be executable
- All your modules should be documented: python3 -c 'print(**import**("my_module").**doc**)'
- Your code should not be executed when imported (by using if **name** == "**main**":)
- You are not allowed to use python’s library Markdown.

## Tasks

### 0. Start a script

**#advanced**
Write a script markdown2html.py that takes an argument 2 strings:

- First argument is the name of the Markdown file
- Second argument is the output file name
  Requirements:
- If the number of arguments is less than 2: print in STDERR Usage: ./markdown2html.py README.md README.html and exit 1
- If the Markdown file doesn’t exist: print in STDER Missing <filename> and exit 1
- Otherwise, print nothing and exit 0

ddddd

---

### 1. Headings

**#advanced**  
Improve `markdown2html.py` by parsing Heading Markdown syntax for generating HTML.

**Syntax:**  
| Markdown | HTML Generated |
|-------------------------------|----------------------------------|
| `# Heading level 1` | `<h1>Heading level 1</h1>` |
| `## Heading level 2` | `<h2>Heading level 2</h2>` |
| `### Heading level 3` | `<h3>Heading level 3</h3>` |
| `#### Heading level 4` | `<h4>Heading level 4</h4>` |
| `##### Heading level 5` | `<h5>Heading level 5</h5>` |
| `###### Heading level 6` | `<h6>Heading level 6</h6>` |

---

### 2. Unordered listing

**#advanced**  
Improve `markdown2html.py` by parsing unordered listing Markdown syntax for generating HTML.

**Syntax:**  
Markdown:

```markdown
- Hello
- Bye
```

HTML generated:

```html
<ul>
  <li>Hello</li>
  <li>Bye</li>
</ul>
```

---

### 3. Ordered listing

**#advanced**  
Improve `markdown2html.py` by parsing ordered listing Markdown syntax for generating HTML.

**Syntax:**  
Markdown:

```markdown
1. Hello
2. Bye
```

HTML generated:

```html
<ol>
  <li>Hello</li>
  <li>Bye</li>
</ol>
```

---

### 4. Simple text

**#advanced**  
Improve `markdown2html.py` by parsing paragraph syntax for generating HTML.

**Syntax:**  
Markdown:

```markdown
Hello

I'm a text
with 2 lines
```

HTML generated:

```html
<p>Hello</p>
<p>
  I'm a text
  <br />
  with 2 lines
</p>
```

---

### 5. Bold and emphasis text

**#advanced**  
Improve `markdown2html.py` by parsing bold and emphasized text Markdown syntax for generating HTML.

**Syntax:**  
| Markdown | HTML Generated |
|----------------------|---------------------|
| `**Hello**` | `<b>Hello</b>` |
| `__Hello__` | `<em>Hello</em>` |

---

### 6. ... but why??

**#advanced**  
Improve `markdown2html.py` by parsing additional complex Markdown syntax for generating HTML.

**Tasks:**

1. Convert `[[Hello]]` into its MD5 hash (in lowercase):
   - Markdown: `[[Hello]]`
   - HTML: `8b1a9953c4611296a827abf8c47804d7`
2. Convert `((Hello Chicago))` by removing all occurrences of `c` (case-insensitive):
   - Markdown: `((Hello Chicago))`
   - HTML: `Hello hiago`
