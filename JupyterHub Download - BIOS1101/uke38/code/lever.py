"""
FIXME
* Programmatically extract notebook filename, see below
  * until then: catch notebook no in the right folder, which causes an error
    in save_notebook()
* Maybe include username in filename and/or inside notebook?
* How to get rid of `<IPython.core.display.Javascript object>` after saving oppgave.ipynb?
"""

"""
Extract one exercise from a notebook and write it to a new notebook.
Students are asked to deliver this new notebook.
The exercise to be delivered indciated with html comments in the notebook:
- start: `<!-- innleveringsoppgave - begin -->`
- end: `### Levere denne innleveringsoppgave`

Workflow:
* Save the notebook
* Loop through all cells for the notebook
* Look for start and end of innleveringsoppgave
* Collect cells inbetween these
* Write a new notebook with only these cells
"""

import pathlib
import os, sys
import json
import time
from IPython.display import display, Javascript
import hashlib

def save_notebook(file_path):
    """
    Programmatically save the oppgaver.ipynb notebook
    before creating innlevering.ipynb.
    From https://stackoverflow.com/questions/32237275/save-an-ipython-notebook-programmatically-from-within-itself
    """

    start_md5 = hashlib.md5(open(file_path,'rb').read()).hexdigest()
    display(Javascript('IPython.notebook.save_checkpoint();'))
    current_md5 = start_md5
    
    while start_md5 == current_md5:
        time.sleep(1)
        current_md5 = hashlib.md5(open(file_path,'rb').read()).hexdigest()

def is_innlevering(cell):
    """
    Determines whether a cell is the start of the Innleveringsoppgave.
    The cell's source should start with a heading indicating this.
    """
    for element in cell['source']:
        if element.startswith("## Innleveringsoppgave\n"): #("## Innleveringsoppgave:"):
            return True
    return False

# misc entries for notebooks
misc = {
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

path = pathlib.PurePath(os.getcwd())
uke = path.name

# på jupyterhub starter dette med 'uke'
uke = uke.replace("uke", "")

# Name of this notebook
## FUTURE implement ipynbname to get notebook name
## https://github.com/msm1089/ipynbname
exercise_notebook = uke + ".oppgaver.ipynb"

# Save notebook first
save_notebook(exercise_notebook)

# name of notebook to produce
deliver_notebook = uke + ".innlevering.ipynb"

# lists
cells = [] # all cell info; no longer in use
cells_sources = [] # containts 'source' entry only
cells_deliver = [] # exercise to be extracted
# add title
cells_deliver.append(
  {
   "cell_type": "markdown",
   "id": "ad33e63f",
   "metadata": {},
   "source": [
    f"## Innleveringsoppgave uke {uke}\n",
    "\n",
    "<div class=\"alert alert-block alert-info\">\n",
    "Denne notebook filen skal bare lastes opp til Canvas.\n",
    "Du skal ikke gjøre endringer i denne notebooken!\n",
    "</div>"
   ]
  }
)

# extract cells
extract = False
with open(exercise_notebook, encoding="utf-8") as f:
    ff = json.load(f)
    for cell in ff['cells']:
        cells.append(cell)
        source = cell['source']
        cells_sources.append(source)
        if is_innlevering(cell):
            extract = True
        elif "### Levere denne innleveringsoppgaven\n" in source:
            extract = False
        elif extract:
            # make all cells uneditable
            cell['metadata']['editable'] = False
            cells_deliver.append(cell)

# set up json for new notebook
new_nb = {}
# add cells first
new_nb['cells'] = cells_deliver
# add metadata
new_nb.update(misc)

# write to file
with open(deliver_notebook, 'w') as f_out:
    f_out.write(json.dumps(new_nb))

# notify user
print(f"Lagret innleveringsoppgaven i notebook fil '{deliver_notebook}',")
print("som nå kan lastes opp til Canvas.")
print("Husk å legge ditt navn til filnavnet!")