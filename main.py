Run python main.py
Iniciando o Robô Afiliado...
Traceback (most recent call last):
  File "/home/runner/work/obo-afiliado/obo-afiliado/main.py", line 23, in <module>
    testar_robo()
  File "/home/runner/work/obo-afiliado/obo-afiliado/main.py", line 13, in testar_robo
    resposta = client.models.generate_content(
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/google/genai/models.py", line 6641, in generate_content
    response = self._generate_content(
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/google/genai/models.py", line 5067, in _generate_content
    response = self._api_client.request(
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/google/genai/_api_client.py", line 1700, in request
    response = self._request(http_request, http_options, stream=False)
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/google/genai/_api_client.py", line 1487, in _request
    return self._retry(self._request_once, http_request, stream)  # type: ignore[no-any-return]
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/tenacity/__init__.py", line 470, in __call__
    do = self.iter(retry_state=retry_state)
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/tenacity/__init__.py", line 371, in iter
    result = action(retry_state)
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/tenacity/__init__.py", line 413, in exc_check
    raise retry_exc.reraise()
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/tenacity/__init__.py", line 184, in reraise
    raise self.last_attempt.result()
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/concurrent/futures/_base.py", line 451, in result
    return self.__get_result()
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/concurrent/futures/_base.py", line 403, in __get_result
    raise self._exception
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/tenacity/__init__.py", line 473, in __call__
    result = fn(*args, **kwargs)
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/google/genai/_api_client.py", line 1464, in _request_once
    errors.APIError.raise_for_response(response)
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/google/genai/errors.py", line 155, in raise_for_response
    cls.raise_error(response.status_code, response_json, response)
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/google/genai/errors.py", line 184, in raise_error
    raise ClientError(status_code, response_json, response)
google.genai.errors.ClientError: 404 NOT_FOUND. {'error': {'code': 404, 'message': 'models/gemini-1.5-flash is not found for API version v1beta, or is not supported for generateContent. Call ModelService.ListModels to see the list of available models and their supported methods.', 'status': 'NOT_FOUND'}}
Error: Process completed with exit code 1.
