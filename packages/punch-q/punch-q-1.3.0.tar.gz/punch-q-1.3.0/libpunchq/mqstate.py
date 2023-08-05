import click

from libpunchq.exceptions import MissingArgumentsException


class State(object):
    """
        A Base state class
    """

    def dictionary_updater(self, *data, **kwargs):
        """
            Update the MQState using a new dictionary and optional
            extra kwargs.

            :param data:
            :param kwargs:
            :return:
        """

        for d in data:
            for key in d:
                if d[key] is not None:
                    setattr(self, key, d[key])

        for key in kwargs:
            if kwargs[key] is not None:
                setattr(self, key, kwargs[key])


class MQState(State):
    """
        The state for an MQ connection
    """

    def __init__(self):
        self.host = None
        self.port = None
        self.qm_name = None
        self.channel = None
        self.username = None
        self.password = None
        self.mcauser = None

        # arbitrary settings. This should not really be here
        # but hey...
        self.table_width = None

    def get_host(self):
        """
            Return the host information in the format:
                hostname(port)

            :return:
        """

        return '{0}({1})'.format(self.host, self.port)

    def validate(self, keys):
        """
            Validate the MQ state by checking that the
            supplied list of keys does not have None
            values.

            :param keys:
            :return:
        """

        # ensure we have everything we need
        if None in [v for k, v in vars(mqstate).items() if k in keys]:
            click.secho('Queue manager configuration object: {0}'.format(self), dim=True)
            click.secho('Not all of the required MQ arguments are '
                        'set via flags or config file options: {0}'.format(', '.join(keys)), fg='red')

            raise MissingArgumentsException

    def __repr__(self):
        return '<Host: {0}, Port: {1}, QMName: {2}, Channel: {3}>'.format(self.host, self.port, self.qm_name,
                                                                          self.channel)


mqstate = MQState()
