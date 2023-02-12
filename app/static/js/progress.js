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
				console.log(respJSON);
				setTimeout(doFetch, respJSON.retry_after_s * 1000)
			} else if (respJSON.responseStatus == 303) {
				console.log("Finished!");
				console.log(respJSON);
			}
		}
	)
}

doFetch();