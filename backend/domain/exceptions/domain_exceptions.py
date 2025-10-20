class DomainException(Exception):
    pass


class FeatureNotFoundException(DomainException):
    def __init__(self, feature_id: str):
        self.feature_id = feature_id
        super().__init__(f"Feature with id {feature_id} not found")


class DuplicateVoteException(DomainException):
    def __init__(self, feature_id: str, user_identifier: str):
        self.feature_id = feature_id
        self.user_identifier = user_identifier
        super().__init__(
            f"User {user_identifier} has already voted for feature {feature_id}"
        )


class InvalidFeatureDataException(DomainException):
    pass
