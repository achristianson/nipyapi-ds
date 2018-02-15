# coding: utf-8

"""
    NiFi Rest Api

    The Rest Api provides programmatic access to command and control a NiFi instance in real time. Start and                                              stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.5.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ProcessGroupStatusSnapshotDTO(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'name': 'str',
        'connection_status_snapshots': 'list[ConnectionStatusSnapshotEntity]',
        'processor_status_snapshots': 'list[ProcessorStatusSnapshotEntity]',
        'process_group_status_snapshots': 'list[ProcessGroupStatusSnapshotEntity]',
        'remote_process_group_status_snapshots': 'list[RemoteProcessGroupStatusSnapshotEntity]',
        'input_port_status_snapshots': 'list[PortStatusSnapshotEntity]',
        'output_port_status_snapshots': 'list[PortStatusSnapshotEntity]',
        'versioned_flow_state': 'str',
        'flow_files_in': 'int',
        'bytes_in': 'int',
        'input': 'str',
        'flow_files_queued': 'int',
        'bytes_queued': 'int',
        'queued': 'str',
        'queued_count': 'str',
        'queued_size': 'str',
        'bytes_read': 'int',
        'read': 'str',
        'bytes_written': 'int',
        'written': 'str',
        'flow_files_out': 'int',
        'bytes_out': 'int',
        'output': 'str',
        'flow_files_transferred': 'int',
        'bytes_transferred': 'int',
        'transferred': 'str',
        'bytes_received': 'int',
        'flow_files_received': 'int',
        'received': 'str',
        'bytes_sent': 'int',
        'flow_files_sent': 'int',
        'sent': 'str',
        'active_thread_count': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'connection_status_snapshots': 'connectionStatusSnapshots',
        'processor_status_snapshots': 'processorStatusSnapshots',
        'process_group_status_snapshots': 'processGroupStatusSnapshots',
        'remote_process_group_status_snapshots': 'remoteProcessGroupStatusSnapshots',
        'input_port_status_snapshots': 'inputPortStatusSnapshots',
        'output_port_status_snapshots': 'outputPortStatusSnapshots',
        'versioned_flow_state': 'versionedFlowState',
        'flow_files_in': 'flowFilesIn',
        'bytes_in': 'bytesIn',
        'input': 'input',
        'flow_files_queued': 'flowFilesQueued',
        'bytes_queued': 'bytesQueued',
        'queued': 'queued',
        'queued_count': 'queuedCount',
        'queued_size': 'queuedSize',
        'bytes_read': 'bytesRead',
        'read': 'read',
        'bytes_written': 'bytesWritten',
        'written': 'written',
        'flow_files_out': 'flowFilesOut',
        'bytes_out': 'bytesOut',
        'output': 'output',
        'flow_files_transferred': 'flowFilesTransferred',
        'bytes_transferred': 'bytesTransferred',
        'transferred': 'transferred',
        'bytes_received': 'bytesReceived',
        'flow_files_received': 'flowFilesReceived',
        'received': 'received',
        'bytes_sent': 'bytesSent',
        'flow_files_sent': 'flowFilesSent',
        'sent': 'sent',
        'active_thread_count': 'activeThreadCount'
    }

    def __init__(self, id=None, name=None, connection_status_snapshots=None, processor_status_snapshots=None, process_group_status_snapshots=None, remote_process_group_status_snapshots=None, input_port_status_snapshots=None, output_port_status_snapshots=None, versioned_flow_state=None, flow_files_in=None, bytes_in=None, input=None, flow_files_queued=None, bytes_queued=None, queued=None, queued_count=None, queued_size=None, bytes_read=None, read=None, bytes_written=None, written=None, flow_files_out=None, bytes_out=None, output=None, flow_files_transferred=None, bytes_transferred=None, transferred=None, bytes_received=None, flow_files_received=None, received=None, bytes_sent=None, flow_files_sent=None, sent=None, active_thread_count=None):
        """
        ProcessGroupStatusSnapshotDTO - a model defined in Swagger
        """

        self._id = None
        self._name = None
        self._connection_status_snapshots = None
        self._processor_status_snapshots = None
        self._process_group_status_snapshots = None
        self._remote_process_group_status_snapshots = None
        self._input_port_status_snapshots = None
        self._output_port_status_snapshots = None
        self._versioned_flow_state = None
        self._flow_files_in = None
        self._bytes_in = None
        self._input = None
        self._flow_files_queued = None
        self._bytes_queued = None
        self._queued = None
        self._queued_count = None
        self._queued_size = None
        self._bytes_read = None
        self._read = None
        self._bytes_written = None
        self._written = None
        self._flow_files_out = None
        self._bytes_out = None
        self._output = None
        self._flow_files_transferred = None
        self._bytes_transferred = None
        self._transferred = None
        self._bytes_received = None
        self._flow_files_received = None
        self._received = None
        self._bytes_sent = None
        self._flow_files_sent = None
        self._sent = None
        self._active_thread_count = None

        if id is not None:
          self.id = id
        if name is not None:
          self.name = name
        if connection_status_snapshots is not None:
          self.connection_status_snapshots = connection_status_snapshots
        if processor_status_snapshots is not None:
          self.processor_status_snapshots = processor_status_snapshots
        if process_group_status_snapshots is not None:
          self.process_group_status_snapshots = process_group_status_snapshots
        if remote_process_group_status_snapshots is not None:
          self.remote_process_group_status_snapshots = remote_process_group_status_snapshots
        if input_port_status_snapshots is not None:
          self.input_port_status_snapshots = input_port_status_snapshots
        if output_port_status_snapshots is not None:
          self.output_port_status_snapshots = output_port_status_snapshots
        if versioned_flow_state is not None:
          self.versioned_flow_state = versioned_flow_state
        if flow_files_in is not None:
          self.flow_files_in = flow_files_in
        if bytes_in is not None:
          self.bytes_in = bytes_in
        if input is not None:
          self.input = input
        if flow_files_queued is not None:
          self.flow_files_queued = flow_files_queued
        if bytes_queued is not None:
          self.bytes_queued = bytes_queued
        if queued is not None:
          self.queued = queued
        if queued_count is not None:
          self.queued_count = queued_count
        if queued_size is not None:
          self.queued_size = queued_size
        if bytes_read is not None:
          self.bytes_read = bytes_read
        if read is not None:
          self.read = read
        if bytes_written is not None:
          self.bytes_written = bytes_written
        if written is not None:
          self.written = written
        if flow_files_out is not None:
          self.flow_files_out = flow_files_out
        if bytes_out is not None:
          self.bytes_out = bytes_out
        if output is not None:
          self.output = output
        if flow_files_transferred is not None:
          self.flow_files_transferred = flow_files_transferred
        if bytes_transferred is not None:
          self.bytes_transferred = bytes_transferred
        if transferred is not None:
          self.transferred = transferred
        if bytes_received is not None:
          self.bytes_received = bytes_received
        if flow_files_received is not None:
          self.flow_files_received = flow_files_received
        if received is not None:
          self.received = received
        if bytes_sent is not None:
          self.bytes_sent = bytes_sent
        if flow_files_sent is not None:
          self.flow_files_sent = flow_files_sent
        if sent is not None:
          self.sent = sent
        if active_thread_count is not None:
          self.active_thread_count = active_thread_count

    @property
    def id(self):
        """
        Gets the id of this ProcessGroupStatusSnapshotDTO.
        The id of the process group.

        :return: The id of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ProcessGroupStatusSnapshotDTO.
        The id of the process group.

        :param id: The id of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ProcessGroupStatusSnapshotDTO.
        The name of this process group.

        :return: The name of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ProcessGroupStatusSnapshotDTO.
        The name of this process group.

        :param name: The name of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._name = name

    @property
    def connection_status_snapshots(self):
        """
        Gets the connection_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all conenctions in the process group.

        :return: The connection_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :rtype: list[ConnectionStatusSnapshotEntity]
        """
        return self._connection_status_snapshots

    @connection_status_snapshots.setter
    def connection_status_snapshots(self, connection_status_snapshots):
        """
        Sets the connection_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all conenctions in the process group.

        :param connection_status_snapshots: The connection_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :type: list[ConnectionStatusSnapshotEntity]
        """

        self._connection_status_snapshots = connection_status_snapshots

    @property
    def processor_status_snapshots(self):
        """
        Gets the processor_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all processors in the process group.

        :return: The processor_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :rtype: list[ProcessorStatusSnapshotEntity]
        """
        return self._processor_status_snapshots

    @processor_status_snapshots.setter
    def processor_status_snapshots(self, processor_status_snapshots):
        """
        Sets the processor_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all processors in the process group.

        :param processor_status_snapshots: The processor_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :type: list[ProcessorStatusSnapshotEntity]
        """

        self._processor_status_snapshots = processor_status_snapshots

    @property
    def process_group_status_snapshots(self):
        """
        Gets the process_group_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all process groups in the process group.

        :return: The process_group_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :rtype: list[ProcessGroupStatusSnapshotEntity]
        """
        return self._process_group_status_snapshots

    @process_group_status_snapshots.setter
    def process_group_status_snapshots(self, process_group_status_snapshots):
        """
        Sets the process_group_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all process groups in the process group.

        :param process_group_status_snapshots: The process_group_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :type: list[ProcessGroupStatusSnapshotEntity]
        """

        self._process_group_status_snapshots = process_group_status_snapshots

    @property
    def remote_process_group_status_snapshots(self):
        """
        Gets the remote_process_group_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all remote process groups in the process group.

        :return: The remote_process_group_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :rtype: list[RemoteProcessGroupStatusSnapshotEntity]
        """
        return self._remote_process_group_status_snapshots

    @remote_process_group_status_snapshots.setter
    def remote_process_group_status_snapshots(self, remote_process_group_status_snapshots):
        """
        Sets the remote_process_group_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all remote process groups in the process group.

        :param remote_process_group_status_snapshots: The remote_process_group_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :type: list[RemoteProcessGroupStatusSnapshotEntity]
        """

        self._remote_process_group_status_snapshots = remote_process_group_status_snapshots

    @property
    def input_port_status_snapshots(self):
        """
        Gets the input_port_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all input ports in the process group.

        :return: The input_port_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :rtype: list[PortStatusSnapshotEntity]
        """
        return self._input_port_status_snapshots

    @input_port_status_snapshots.setter
    def input_port_status_snapshots(self, input_port_status_snapshots):
        """
        Sets the input_port_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all input ports in the process group.

        :param input_port_status_snapshots: The input_port_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :type: list[PortStatusSnapshotEntity]
        """

        self._input_port_status_snapshots = input_port_status_snapshots

    @property
    def output_port_status_snapshots(self):
        """
        Gets the output_port_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all output ports in the process group.

        :return: The output_port_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :rtype: list[PortStatusSnapshotEntity]
        """
        return self._output_port_status_snapshots

    @output_port_status_snapshots.setter
    def output_port_status_snapshots(self, output_port_status_snapshots):
        """
        Sets the output_port_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        The status of all output ports in the process group.

        :param output_port_status_snapshots: The output_port_status_snapshots of this ProcessGroupStatusSnapshotDTO.
        :type: list[PortStatusSnapshotEntity]
        """

        self._output_port_status_snapshots = output_port_status_snapshots

    @property
    def versioned_flow_state(self):
        """
        Gets the versioned_flow_state of this ProcessGroupStatusSnapshotDTO.
        The current state of the Process Group, as it relates to the Versioned Flow

        :return: The versioned_flow_state of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._versioned_flow_state

    @versioned_flow_state.setter
    def versioned_flow_state(self, versioned_flow_state):
        """
        Sets the versioned_flow_state of this ProcessGroupStatusSnapshotDTO.
        The current state of the Process Group, as it relates to the Versioned Flow

        :param versioned_flow_state: The versioned_flow_state of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """
        # allowed_values = ["LOCALLY_MODIFIED_DESCENDANT", "LOCALLY_MODIFIED", "STALE", "LOCALLY_MODIFIED_AND_STALE", "UP_TO_DATE"]
        # https://issues.apache.org/jira/browse/NIFI-4859
        allowed_values = ["LOCALLY_MODIFIED_DESCENDANT", "LOCALLY_MODIFIED",
                          "STALE", "LOCALLY_MODIFIED_AND_STALE", "UP_TO_DATE",
                          "SYNC_FAILURE"]
        if versioned_flow_state not in allowed_values:
            raise ValueError(
                "Invalid value for `versioned_flow_state` ({0}), must be one of {1}"
                .format(versioned_flow_state, allowed_values)
            )

        self._versioned_flow_state = versioned_flow_state

    @property
    def flow_files_in(self):
        """
        Gets the flow_files_in of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles that have come into this ProcessGroup in the last 5 minutes

        :return: The flow_files_in of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_in

    @flow_files_in.setter
    def flow_files_in(self, flow_files_in):
        """
        Sets the flow_files_in of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles that have come into this ProcessGroup in the last 5 minutes

        :param flow_files_in: The flow_files_in of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_in = flow_files_in

    @property
    def bytes_in(self):
        """
        Gets the bytes_in of this ProcessGroupStatusSnapshotDTO.
        The number of bytes that have come into this ProcessGroup in the last 5 minutes

        :return: The bytes_in of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_in

    @bytes_in.setter
    def bytes_in(self, bytes_in):
        """
        Sets the bytes_in of this ProcessGroupStatusSnapshotDTO.
        The number of bytes that have come into this ProcessGroup in the last 5 minutes

        :param bytes_in: The bytes_in of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._bytes_in = bytes_in

    @property
    def input(self):
        """
        Gets the input of this ProcessGroupStatusSnapshotDTO.
        The input count/size for the process group in the last 5 minutes (pretty printed).

        :return: The input of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._input

    @input.setter
    def input(self, input):
        """
        Sets the input of this ProcessGroupStatusSnapshotDTO.
        The input count/size for the process group in the last 5 minutes (pretty printed).

        :param input: The input of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._input = input

    @property
    def flow_files_queued(self):
        """
        Gets the flow_files_queued of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles that are queued up in this ProcessGroup right now

        :return: The flow_files_queued of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_queued

    @flow_files_queued.setter
    def flow_files_queued(self, flow_files_queued):
        """
        Sets the flow_files_queued of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles that are queued up in this ProcessGroup right now

        :param flow_files_queued: The flow_files_queued of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_queued = flow_files_queued

    @property
    def bytes_queued(self):
        """
        Gets the bytes_queued of this ProcessGroupStatusSnapshotDTO.
        The number of bytes that are queued up in this ProcessGroup right now

        :return: The bytes_queued of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_queued

    @bytes_queued.setter
    def bytes_queued(self, bytes_queued):
        """
        Sets the bytes_queued of this ProcessGroupStatusSnapshotDTO.
        The number of bytes that are queued up in this ProcessGroup right now

        :param bytes_queued: The bytes_queued of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._bytes_queued = bytes_queued

    @property
    def queued(self):
        """
        Gets the queued of this ProcessGroupStatusSnapshotDTO.
        The count/size that is queued in the the process group.

        :return: The queued of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._queued

    @queued.setter
    def queued(self, queued):
        """
        Sets the queued of this ProcessGroupStatusSnapshotDTO.
        The count/size that is queued in the the process group.

        :param queued: The queued of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._queued = queued

    @property
    def queued_count(self):
        """
        Gets the queued_count of this ProcessGroupStatusSnapshotDTO.
        The count that is queued for the process group.

        :return: The queued_count of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._queued_count

    @queued_count.setter
    def queued_count(self, queued_count):
        """
        Sets the queued_count of this ProcessGroupStatusSnapshotDTO.
        The count that is queued for the process group.

        :param queued_count: The queued_count of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._queued_count = queued_count

    @property
    def queued_size(self):
        """
        Gets the queued_size of this ProcessGroupStatusSnapshotDTO.
        The size that is queued for the process group.

        :return: The queued_size of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._queued_size

    @queued_size.setter
    def queued_size(self, queued_size):
        """
        Sets the queued_size of this ProcessGroupStatusSnapshotDTO.
        The size that is queued for the process group.

        :param queued_size: The queued_size of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._queued_size = queued_size

    @property
    def bytes_read(self):
        """
        Gets the bytes_read of this ProcessGroupStatusSnapshotDTO.
        The number of bytes read by components in this ProcessGroup in the last 5 minutes

        :return: The bytes_read of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_read

    @bytes_read.setter
    def bytes_read(self, bytes_read):
        """
        Sets the bytes_read of this ProcessGroupStatusSnapshotDTO.
        The number of bytes read by components in this ProcessGroup in the last 5 minutes

        :param bytes_read: The bytes_read of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._bytes_read = bytes_read

    @property
    def read(self):
        """
        Gets the read of this ProcessGroupStatusSnapshotDTO.
        The number of bytes read in the last 5 minutes.

        :return: The read of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._read

    @read.setter
    def read(self, read):
        """
        Sets the read of this ProcessGroupStatusSnapshotDTO.
        The number of bytes read in the last 5 minutes.

        :param read: The read of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._read = read

    @property
    def bytes_written(self):
        """
        Gets the bytes_written of this ProcessGroupStatusSnapshotDTO.
        The number of bytes written by components in this ProcessGroup in the last 5 minutes

        :return: The bytes_written of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_written

    @bytes_written.setter
    def bytes_written(self, bytes_written):
        """
        Sets the bytes_written of this ProcessGroupStatusSnapshotDTO.
        The number of bytes written by components in this ProcessGroup in the last 5 minutes

        :param bytes_written: The bytes_written of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._bytes_written = bytes_written

    @property
    def written(self):
        """
        Gets the written of this ProcessGroupStatusSnapshotDTO.
        The number of bytes written in the last 5 minutes.

        :return: The written of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._written

    @written.setter
    def written(self, written):
        """
        Sets the written of this ProcessGroupStatusSnapshotDTO.
        The number of bytes written in the last 5 minutes.

        :param written: The written of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._written = written

    @property
    def flow_files_out(self):
        """
        Gets the flow_files_out of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles transferred out of this ProcessGroup in the last 5 minutes

        :return: The flow_files_out of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_out

    @flow_files_out.setter
    def flow_files_out(self, flow_files_out):
        """
        Sets the flow_files_out of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles transferred out of this ProcessGroup in the last 5 minutes

        :param flow_files_out: The flow_files_out of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_out = flow_files_out

    @property
    def bytes_out(self):
        """
        Gets the bytes_out of this ProcessGroupStatusSnapshotDTO.
        The number of bytes transferred out of this ProcessGroup in the last 5 minutes

        :return: The bytes_out of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_out

    @bytes_out.setter
    def bytes_out(self, bytes_out):
        """
        Sets the bytes_out of this ProcessGroupStatusSnapshotDTO.
        The number of bytes transferred out of this ProcessGroup in the last 5 minutes

        :param bytes_out: The bytes_out of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._bytes_out = bytes_out

    @property
    def output(self):
        """
        Gets the output of this ProcessGroupStatusSnapshotDTO.
        The output count/size for the process group in the last 5 minutes.

        :return: The output of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._output

    @output.setter
    def output(self, output):
        """
        Sets the output of this ProcessGroupStatusSnapshotDTO.
        The output count/size for the process group in the last 5 minutes.

        :param output: The output of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._output = output

    @property
    def flow_files_transferred(self):
        """
        Gets the flow_files_transferred of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles transferred in this ProcessGroup in the last 5 minutes

        :return: The flow_files_transferred of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_transferred

    @flow_files_transferred.setter
    def flow_files_transferred(self, flow_files_transferred):
        """
        Sets the flow_files_transferred of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles transferred in this ProcessGroup in the last 5 minutes

        :param flow_files_transferred: The flow_files_transferred of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_transferred = flow_files_transferred

    @property
    def bytes_transferred(self):
        """
        Gets the bytes_transferred of this ProcessGroupStatusSnapshotDTO.
        The number of bytes transferred in this ProcessGroup in the last 5 minutes

        :return: The bytes_transferred of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_transferred

    @bytes_transferred.setter
    def bytes_transferred(self, bytes_transferred):
        """
        Sets the bytes_transferred of this ProcessGroupStatusSnapshotDTO.
        The number of bytes transferred in this ProcessGroup in the last 5 minutes

        :param bytes_transferred: The bytes_transferred of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._bytes_transferred = bytes_transferred

    @property
    def transferred(self):
        """
        Gets the transferred of this ProcessGroupStatusSnapshotDTO.
        The count/size transferred to/from queues in the process group in the last 5 minutes.

        :return: The transferred of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._transferred

    @transferred.setter
    def transferred(self, transferred):
        """
        Sets the transferred of this ProcessGroupStatusSnapshotDTO.
        The count/size transferred to/from queues in the process group in the last 5 minutes.

        :param transferred: The transferred of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._transferred = transferred

    @property
    def bytes_received(self):
        """
        Gets the bytes_received of this ProcessGroupStatusSnapshotDTO.
        The number of bytes received from external sources by components within this ProcessGroup in the last 5 minutes

        :return: The bytes_received of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_received

    @bytes_received.setter
    def bytes_received(self, bytes_received):
        """
        Sets the bytes_received of this ProcessGroupStatusSnapshotDTO.
        The number of bytes received from external sources by components within this ProcessGroup in the last 5 minutes

        :param bytes_received: The bytes_received of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._bytes_received = bytes_received

    @property
    def flow_files_received(self):
        """
        Gets the flow_files_received of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles received from external sources by components within this ProcessGroup in the last 5 minutes

        :return: The flow_files_received of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_received

    @flow_files_received.setter
    def flow_files_received(self, flow_files_received):
        """
        Sets the flow_files_received of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles received from external sources by components within this ProcessGroup in the last 5 minutes

        :param flow_files_received: The flow_files_received of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_received = flow_files_received

    @property
    def received(self):
        """
        Gets the received of this ProcessGroupStatusSnapshotDTO.
        The count/size sent to the process group in the last 5 minutes.

        :return: The received of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._received

    @received.setter
    def received(self, received):
        """
        Sets the received of this ProcessGroupStatusSnapshotDTO.
        The count/size sent to the process group in the last 5 minutes.

        :param received: The received of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._received = received

    @property
    def bytes_sent(self):
        """
        Gets the bytes_sent of this ProcessGroupStatusSnapshotDTO.
        The number of bytes sent to an external sink by components within this ProcessGroup in the last 5 minutes

        :return: The bytes_sent of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_sent

    @bytes_sent.setter
    def bytes_sent(self, bytes_sent):
        """
        Sets the bytes_sent of this ProcessGroupStatusSnapshotDTO.
        The number of bytes sent to an external sink by components within this ProcessGroup in the last 5 minutes

        :param bytes_sent: The bytes_sent of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._bytes_sent = bytes_sent

    @property
    def flow_files_sent(self):
        """
        Gets the flow_files_sent of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles sent to an external sink by components within this ProcessGroup in the last 5 minutes

        :return: The flow_files_sent of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_sent

    @flow_files_sent.setter
    def flow_files_sent(self, flow_files_sent):
        """
        Sets the flow_files_sent of this ProcessGroupStatusSnapshotDTO.
        The number of FlowFiles sent to an external sink by components within this ProcessGroup in the last 5 minutes

        :param flow_files_sent: The flow_files_sent of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_sent = flow_files_sent

    @property
    def sent(self):
        """
        Gets the sent of this ProcessGroupStatusSnapshotDTO.
        The count/size sent from this process group in the last 5 minutes.

        :return: The sent of this ProcessGroupStatusSnapshotDTO.
        :rtype: str
        """
        return self._sent

    @sent.setter
    def sent(self, sent):
        """
        Sets the sent of this ProcessGroupStatusSnapshotDTO.
        The count/size sent from this process group in the last 5 minutes.

        :param sent: The sent of this ProcessGroupStatusSnapshotDTO.
        :type: str
        """

        self._sent = sent

    @property
    def active_thread_count(self):
        """
        Gets the active_thread_count of this ProcessGroupStatusSnapshotDTO.
        The active thread count for this process group.

        :return: The active_thread_count of this ProcessGroupStatusSnapshotDTO.
        :rtype: int
        """
        return self._active_thread_count

    @active_thread_count.setter
    def active_thread_count(self, active_thread_count):
        """
        Sets the active_thread_count of this ProcessGroupStatusSnapshotDTO.
        The active thread count for this process group.

        :param active_thread_count: The active_thread_count of this ProcessGroupStatusSnapshotDTO.
        :type: int
        """

        self._active_thread_count = active_thread_count

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, ProcessGroupStatusSnapshotDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
