<script context="module">
	/**
	 *
	 * @component QR Scanner
	 *
	 */

	import { Html5Qrcode } from "html5-qrcode";
	import Alert from "./Alert.svelte";
	import Modal from "./Modal.svelte";
	import axios from "axios";

	let html5Qrcode, result, scanning, loading;

	let handler = async (userData) => {
		let fetchURL = "/api/validate-id?";

		let data = new FormData();

		data.append("userToken", userData); // Javascript object => FormData object

		try {
			let response = await axios.post(fetchURL, data, {
				headers: {
					"Content-Type": "multipart/form-data",
				},
			});

			//console.log(response.data);

			return response.data;
		} catch (err) {
			console.error("Error: ", err.response);
			return "Error";
		}
	};

	export let init = () => {
		html5Qrcode = new Html5Qrcode("reader");
	};

	let start = () => {
		loading = true;
		html5Qrcode.start(
			{ facingMode: "environment" },
			{ fps: 10 },
			onScanSuccess,
			onScanFailure
		);
		scanning = true;
		loading = false;
	};

	let stop = async () => {
		await html5Qrcode.stop();
		scanning = false;
	};

	let onScanSuccess = async (decodedText, decodedResult) => {
		let data = JSON.parse(decodedText); // convert decoded JSON to JS object
		console.log("Request Data :", data);

		let op = await handler(data); // get result

		//console.log("Response Data :", op);
		result.innerText = op;
	};

	let onScanFailure = (error) => {
		//console.warn(`Code scan error = ${error}`);
	};
</script>

<div
	class="scanner"
	on:click={start}
	data-bs-toggle="modal"
	data-bs-target="#staticBackdrop"
>
	<slot />
</div>

<Modal id={"staticBackdrop"} closeBtnClick={stop}>
	<svelte:fragment slot="header">CVIS - QR SCANNER</svelte:fragment>
	<svelte:fragment slot="body">
		<div id="reader" class="d-flex justify-content-center">
			{#if loading}
				loading
			{/if}
		</div>
	</svelte:fragment>
	<svelte:fragment slot="footer">
		<div class="container-fluid">
			<label for="" class="form-label fw-bold text-primary">
				Result
			</label>
			<Alert color="primary">
				<p bind:this={result} />
			</Alert>
		</div>
	</svelte:fragment>
</Modal>

<style>
	.scanner:hover {
		cursor: pointer;
	}
</style>
