function doFetch() {
	fetch(statusUrl).then(
		(response) => {
			return response.json().then((respJSON) => {
				respJSON.responseStatus = response.status;
				return respJSON;
			});
		}
	).then(
		(respJSON) => {
			if (respJSON.responseStatus == 200) {
				setTimeout(doFetch, respJSON.retry_after_s * 1000)
			} else if (respJSON.responseStatus == 303) {
				window.location.replace(respJSON.resource);
			}
		}
	)
}

doFetch();