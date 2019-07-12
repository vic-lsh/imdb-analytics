package job

import (
	"fmt"
	"testing"
)

func fmtJobStatusErrMsg(input ExtractionJobStatus, expected string, output string) string {
	return fmt.Sprintf("ExtractionJobStatusOutput test failed: \tinputted: %d, \texpected: %s, \treceived: %s\n", input, expected, output)
}

func TestExtractionJobStatusString(t *testing.T) {
	var np ExtractionJobStatus = 1
	npExpectedOut := "Processing"

	var invalidJS ExtractionJobStatus = 100
	invalidJSExpectedOut := fmt.Sprintf("Type Unknown %d", invalidJS)

	if npOut := np.String(); npOut != npExpectedOut {
		t.Error(fmtJobStatusErrMsg(np, npExpectedOut, npOut))
	}

	if invalidJSOut := invalidJS.String(); invalidJSOut != invalidJSExpectedOut {
		t.Error(fmtJobStatusErrMsg(invalidJS, invalidJSExpectedOut, invalidJSOut))
	}
}
