import komand
from .schema import ElasticsearchDeleteInput, ElasticsearchDeleteOutput
# Custom imports below
import subprocess
from sys import argv


class ElasticsearchDelete(komand.Action):

    def __init__(self):
        super(self.__class__, self).__init__(
                name='elasticsearch_delete',
                description='Base64 encoded index name to delete',
                input=ElasticsearchDeleteInput(),
                output=ElasticsearchDeleteOutput())
        self.host = None
        self.password = None

    def run(self, params={}):
        self.host = params.get('host')
        self.password = params.get('password')
        index_name = params.get('index_name')
        command = params.get('command')

        index_name = argv[0]
        command = argv[1]
        if not self.host and not self.password:
            # do the way on the command line
            transfer = subprocess.Popen(['python rc.py es --delete %s %s' % (index_name, command)],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out = transfer.communicate()[0]
            output = str(out)
            return {'results': output}
        elif self.host and self.password:
            # connect via ssh and then execute the commands
            command = 'python /var/lib/automation/rc.py es --delete %s %s' % (index_name, command)
            client = self.connection.client(self.host)
            (stdin, stdout, stderr) = client.exec_command(command)
            stdout_string = "\n".join(stdout.readlines())
            stderr_string = "\n".join(stderr.readlines())
            client.close()
            return {'results': stdout_string + stderr_string}

    def test(self):
        # TODO: Implement test function
        if self.host and self.password:
            client = self.connection.client(self.host)
            client.close()
            return {'results': ''}
        elif not self.host and self.password:
            return {'results': 'Ready to delete ElasticSearch index'}
