package job

import (
	"fmt"
	"testing"
)

func fmtJobStatusErrMsg(input ExtractionJobStatus, expected string, output string) string {
	return fmt.Sprintf("ExtractionJobStatusOutput test failed: \tinputted: %d, \texpected: %s, \treceived: %s\n",
		input, expected, output)
}

func TestJobStatusString(t *testing.T) {
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

func TestJobStatusMarshall(t *testing.T) {
	validCases := map[ExtractionJob]extractionJobMarshalled{
		{ID: 123999811, Name: "GOT", Status: NotProcessed}:       {ID: 123999811, Name: "GOT", Status: "Not processed"},
		{ID: 123999811, Name: "GOT", Status: Processing}:         {ID: 123999811, Name: "GOT", Status: "Processing"},
		{ID: 123999811, Name: "GOT", Status: CompletedSucceeded}: {ID: 123999811, Name: "GOT", Status: "Completed successfully"},
		{ID: 123999811, Name: "GOT", Status: CompletedFailed}:    {ID: 123999811, Name: "GOT", Status: "Failed to complete"},
	}

	for in, expectedOut := range validCases {
		if out := in.marshall(); out != expectedOut {
			t.Errorf("ExtractionJobStatus marshalling test failed: \tinputted: %+v, \texpected: %+v, got: %+v",
				in, expectedOut, out)
		}
	}
}
