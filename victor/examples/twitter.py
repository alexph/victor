from victor import Victor, Workflow
from victor.contrib.readers import BeanstalkReader

workflow = Workflow()

beanstalk = BeanstalkReader()

app = Victor()
app.set_import(beanstalk)
app.register(workflow)
