document.addEventListener("DOMContentLoaded", function () {
    const resultBox = document.getElementById("result");
    const scanner = new Html5Qrcode("reader");
    
    function startScanner() {
        scanner
        .start({ facingMode: "environment" }, { fps: 10, qrbox: 250 }, onScanSuccess, onScanFailure)
        .catch(err => {
            resultBox.innerText = "Camera error: " + err;
            resultBox.className = "fail";
        });
    }
    
    function stopScanner() {
        return scanner.stop().catch(err => {
            console.error("Failed to stop scanner: ", err);
        });
    }
    
    async function onScanSuccess(qrMessage) {
        await stopScanner();
        resultBox.innerText = "Checking...";
        resultBox.className = "";
        
        fetch("/tmp/validate_qr", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ unique_id: qrMessage.trim() })
        })
        .then(res => res.json())
        .then(data => {
            resultBox.innerText = data.message;
            resultBox.className = data.success ? "success" : "fail";
            
            setTimeout(() => {
                resultBox.innerText = "Waiting for scan...";
                resultBox.className = "";
                startScanner();
            }, 2000);
        })
        .catch(err => {
            resultBox.innerText = "Network error";
            resultBox.className = "fail";
            
            setTimeout(() => {
                resultBox.innerText = "Waiting for scan...";
                resultBox.className = "";
                startScanner();
            }, 2000);
        });
    }
    
    function onScanFailure(error) {
        // fail silently
    }
    
    startScanner();
});
