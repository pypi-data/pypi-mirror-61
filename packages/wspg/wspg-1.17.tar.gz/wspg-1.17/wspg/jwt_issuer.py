#
#   Copyright 2018 University of Lancaster
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from typing import Mapping, TYPE_CHECKING

import jwt

from .errors import ClientLeakableError

if TYPE_CHECKING:
    from .application import Application  # noqa


class JWTIssuer:
    def __init__(self, application: 'Application', path: str) -> None:
        self.application = application
        self.path = path

        self.config = application.config[path]

        self.validity_period = int(self.config['validity-period'])

    def decode(self, token: str) -> Mapping[str, str]:
        try:
            claims_set = jwt.decode(token, self.config['secret'], leeway=self.validity_period)
        except jwt.InvalidTokenError as e:
            raise ClientLeakableError("JWT decode error: {}".format(e)) from e

        claims_set['expiry-timestamp'] = claims_set['exp'] + self.validity_period

        return claims_set
