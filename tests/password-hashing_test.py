from json import dumps
from assertpy.assertpy import assert_that
from config import BASE_URI

import requests


def test_setup_is_success():
    # Sending a get request to stats
    response = requests.get(BASE_URI + '/stats')
    response_content = response.json()

    # It should answer on the port 8088 specified in environment variables
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(response_content).extracting('TotalRequests').is_not_empty()
    assert_that(response_content).extracting('AverageTime').is_not_empty()


def test_create_jobid_valid_password():
    # Given a password with only strings
    payload = dumps({
        'password': 'abluemonday'
    })

    # And set default headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # When sending a post request to /hash
    response = requests.post(url=BASE_URI+'/hash', data=payload, headers=headers)

    # Then I get response code - 201 - created
    response_content = response.json()
    assert_that(response.status_code).is_equal_to(requests.codes.created)
    # And response is not empty, it contains the job identifier
    assert_that(response_content).is_not_empty()


def test_create_jobid_empty_password_un_processable_entity():
    # Given a password with only strings
    payload = dumps({
        'password': ''
    })
    # And set default headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # When sending a post request to /hash
    response = requests.post(url=BASE_URI+'/hash', data=payload, headers=headers)

    # Then I get response code - 422 - un processable entity
    response_content = response.json()
    assert_that(response.status_code).is_equal_to(requests.codes.unprocessable_entity)


def test_read_encoded_password():
    # Given I create a hashed password and get job identifier
    jobid = create_jobid()

    # When I read the job identifier
    response = requests.get(BASE_URI + '/hash/' + jobid)

    # Then I get success status
    assert_that(response.status_code).is_equal_to(requests.codes.ok)

    # And I get base64 encoded password
    assert_that(response)\
        .is_not_empty()\
        .contains('RTZdHiWHNRzxkm1plry4JdbhBpo44CVQrTNu85SpVFKFbibYXtl4tW8NMCGbE/WBpwAUiUzJlaKJQIO8m/M9eg==')


def test_read_encoded_password_not_found():
    # Given I have an non-existent jobid
    jobid = 9989

    # When I read the job identifier
    response = requests.get(BASE_URI + '/hash/' + jobid)

    # Then I get not found status code - 404
    assert_that(response.status_code).is_equal_to(requests.codes.not_found)

    # And I get correct message for hash not found
    assert_that(response)\
        .is_not_empty()\
        .contains('Hash not found')


def test_read_total_requests_average_time():
    # Given I sent a get request to stats
    response = requests.get(BASE_URI + '/stats')
    response_content = response.json()

    # Then I get success status
    assert_that(response.status_code).is_equal_to(requests.codes.ok)

    # And get TotalRequests and AverageTime parameters
    assert_that(response_content).extracting('TotalRequests').is_not_empty()
    assert_that(response_content).extracting('AverageTime').is_not_empty()

    # And AverageTime is not 0
    average_time = response_content.extracting('AverageTime')
    assert_that(average_time > 0).is_true()


def test_shutdown_node():
    # Given I define body request for shutdown
    body = 'shutdown'

    # When I send a post shutdown request to /hash
    response = requests.post(url=BASE_URI + '/hash', data=body)

    # Then I get success response code 200
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    # And response is empty
    assert_that(response).is_empty()


def create_jobid():
    # Given a password with only strings
    payload = dumps({
        'password': 'abluemonday'
    })
    # And set default headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # When sending a post request to /hash
    jobid = requests.post(url=BASE_URI+'/hash', data=payload, headers=headers)

    # Then I get response code - 201 - created
    assert_that(jobid.status_code).is_equal_to(requests.codes.created)
    # And response is not empty, it contains the job identifier
    assert_that(jobid).is_not_empty()
    return jobid
