# filetrace

Collect the list of files opened while executing a command

## Usage

```bash
pip3 install --user filetrace
filetrace -- command
```

## Running from the source
```bash
git clone https://github.com/joaompinto/filetrace
cd filetrace
pip3 install --user -r requirements.txt
python3 -m filetrace -- bash -c "true; cat /dev/null"
```
