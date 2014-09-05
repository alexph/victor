from victor import Victor, Workflow


workflow = Workflow()

def read_stream():
    for i in range(100):
        yield i

app = Victor()
app.set_import(read_stream)
app.register(workflow)
