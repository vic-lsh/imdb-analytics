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
		0: NotProcessedMsg,
		1: ProcessingMsg,
		2: CompletedSucceededMsg,
		3: CompletedFailedMsg,
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
		{ID: 123999811, Name: "GOT", Status: NotProcessed}:       {ID: 123999811, Name: "GOT", Status: NotProcessedMsg},
		{ID: 123999811, Name: "GOT", Status: Processing}:         {ID: 123999811, Name: "GOT", Status: ProcessingMsg},
		{ID: 123999811, Name: "GOT", Status: CompletedSucceeded}: {ID: 123999811, Name: "GOT", Status: CompletedSucceededMsg},
		{ID: 123999811, Name: "GOT", Status: CompletedFailed}:    {ID: 123999811, Name: "GOT", Status: CompletedFailedMsg},
	}

	for in, expectedOut := range validCases {
		if out := in.marshall(); out != expectedOut {
			t.Errorf("ExtractionJobStatus marshalling test failed: \n\tinputted: %+v, \n\texpected: %+v, \n\tgot: %+v\n",
				in, expectedOut, out)
		}
	}
}
