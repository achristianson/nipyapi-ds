export function perform_cloud_ops() {
    console.log('requesting run of cloud ops');
    fetch("/api/perform-cloud-ops").then(
        response => response.json().then(
            o => {
                console.log('successfully requested run of cloud ops');
            }
        )
    );
}
