# coding: utf-8

"""
    NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 0.2.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class VersionedFlowSnapshot(object):
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
        'snapshot_metadata': 'VersionedFlowSnapshotMetadata',
        'flow_contents': 'VersionedProcessGroup',
        'flow': 'VersionedFlow',
        'bucket': 'Bucket',
        'latest': 'bool'
    }

    attribute_map = {
        'snapshot_metadata': 'snapshotMetadata',
        'flow_contents': 'flowContents',
        'flow': 'flow',
        'bucket': 'bucket',
        'latest': 'latest'
    }

    def __init__(self, snapshot_metadata=None, flow_contents=None, flow=None, bucket=None, latest=None):
        """
        VersionedFlowSnapshot - a model defined in Swagger
        """

        self._snapshot_metadata = None
        self._flow_contents = None
        self._flow = None
        self._bucket = None
        self._latest = None

        self.snapshot_metadata = snapshot_metadata
        self.flow_contents = flow_contents
        if flow is not None:
          self.flow = flow
        if bucket is not None:
          self.bucket = bucket
        if latest is not None:
          self.latest = latest

    @property
    def snapshot_metadata(self):
        """
        Gets the snapshot_metadata of this VersionedFlowSnapshot.
        The metadata for this snapshot

        :return: The snapshot_metadata of this VersionedFlowSnapshot.
        :rtype: VersionedFlowSnapshotMetadata
        """
        return self._snapshot_metadata

    @snapshot_metadata.setter
    def snapshot_metadata(self, snapshot_metadata):
        """
        Sets the snapshot_metadata of this VersionedFlowSnapshot.
        The metadata for this snapshot

        :param snapshot_metadata: The snapshot_metadata of this VersionedFlowSnapshot.
        :type: VersionedFlowSnapshotMetadata
        """
        if snapshot_metadata is None:
            raise ValueError("Invalid value for `snapshot_metadata`, must not be `None`")

        self._snapshot_metadata = snapshot_metadata

    @property
    def flow_contents(self):
        """
        Gets the flow_contents of this VersionedFlowSnapshot.
        The contents of the versioned flow

        :return: The flow_contents of this VersionedFlowSnapshot.
        :rtype: VersionedProcessGroup
        """
        return self._flow_contents

    @flow_contents.setter
    def flow_contents(self, flow_contents):
        """
        Sets the flow_contents of this VersionedFlowSnapshot.
        The contents of the versioned flow

        :param flow_contents: The flow_contents of this VersionedFlowSnapshot.
        :type: VersionedProcessGroup
        """
        if flow_contents is None:
            raise ValueError("Invalid value for `flow_contents`, must not be `None`")

        self._flow_contents = flow_contents

    @property
    def flow(self):
        """
        Gets the flow of this VersionedFlowSnapshot.
        The flow this snapshot is for

        :return: The flow of this VersionedFlowSnapshot.
        :rtype: VersionedFlow
        """
        return self._flow

    @flow.setter
    def flow(self, flow):
        """
        Sets the flow of this VersionedFlowSnapshot.
        The flow this snapshot is for

        :param flow: The flow of this VersionedFlowSnapshot.
        :type: VersionedFlow
        """

        self._flow = flow

    @property
    def bucket(self):
        """
        Gets the bucket of this VersionedFlowSnapshot.
        The bucket where the flow is located

        :return: The bucket of this VersionedFlowSnapshot.
        :rtype: Bucket
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """
        Sets the bucket of this VersionedFlowSnapshot.
        The bucket where the flow is located

        :param bucket: The bucket of this VersionedFlowSnapshot.
        :type: Bucket
        """

        self._bucket = bucket

    @property
    def latest(self):
        """
        Gets the latest of this VersionedFlowSnapshot.

        :return: The latest of this VersionedFlowSnapshot.
        :rtype: bool
        """
        return self._latest

    @latest.setter
    def latest(self, latest):
        """
        Sets the latest of this VersionedFlowSnapshot.

        :param latest: The latest of this VersionedFlowSnapshot.
        :type: bool
        """

        self._latest = latest

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
        if not isinstance(other, VersionedFlowSnapshot):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
