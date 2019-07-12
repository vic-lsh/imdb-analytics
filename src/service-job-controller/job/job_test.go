package job

import (
	"fmt"
	"testing"
)

func fmtJobStatusErrMsg(input ExtractionJobStatus, expected string, output string) string {
	return fmt.Sprintf("ExtractionJobStatusOutput test failed: \tinputted: %d, \texpected: %s, \treceived: %s\n", input, expected, output)
}

func TestExtractionJobStatusString(t *testing.T) {
	validCases := map[ExtractionJobStatus]string{
		0: "Not processed",
		1: "Processing",
		2: "Completed successfully",
		3: "Failed to complete",
	}
	for in, expectedOut := range validCases {
		if out := in.String(); out != expectedOut {
			t.Error(fmtJobStatusErrMsg(in, expectedOut, out))
		}

	}

	invalidCases := [...]ExtractionJobStatus{-10000, -1, 4, 9, 100}
	for _, in := range invalidCases {
		expectedOut := fmt.Sprintf("Type Unknown %d", in)
		if out := in.String(); out != expectedOut {
			t.Error(fmtJobStatusErrMsg(in, expectedOut, out))
		}
	}
}
