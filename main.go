package main

import (
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/spf13/cobra"
)

var (
	rootCmd = &cobra.Command{ //nolint:gochecknoglobals
		Use:   "aoc [options] <command> [arguments]",
		Short: "AoC CLI Tool",
		Long:  `AoC CLI Tool to help setup a new day of puzzle solving`,
	}
	dayCmd = &cobra.Command{
		Use:   "day [day num]",
		Short: `Setup puzzle template for a given day`,
		RunE:  runDay,
		Args:  cobra.MinimumNArgs(1),
	}
	year = "2023"
)

type Day struct {
	day string
}

func main() {
	rootCmd.AddCommand(dayCmd)
	rootCmd.PersistentFlags().StringP("session", "s", "", "optional session token")

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

}

func runDay(command *cobra.Command, args []string) error {
	session, sessionErr := command.Flags().GetString("session")
	if sessionErr != nil {
		return sessionErr
	}
	if session == "" {
		session = "53616c7465645f5f34b82f39e2d7865d94084c338aeb434b8c1d523807410ea4572825b767ea25ff5bbc4e9b4b384decedbd18a3ef013dccb1d96bcd8fc8a92f"
	}
	day := args[0]

	input, inputErr := getInput(day, session)
	if inputErr != nil {
		return inputErr
	}

	createFileStructure(day, input)

	return nil
}

func createFileStructure(day, input string) error {
	dayDir := "day" + day
	err := os.Mkdir(dayDir, 0755)
	if err != nil {
		return err
	}
	err = os.Mkdir(dayDir+"/test", 0755)
	if err != nil {
		return err
	}

	err = os.WriteFile(dayDir+"/test/input.txt", []byte(input), 0755)
	if err != nil {
		return err
	}

	pyText, err := os.ReadFile("main.tmpl")
	if err != nil {
		return err
	}
	err = os.WriteFile(dayDir+"/main.py", pyText, 0755)
	if err != nil {
		return err
	}

	return nil
}

func getInput(day, session string) (string, error) {
	cookie := &http.Cookie{
		Name:  "session",
		Value: session,
	}
	url := "https://adventofcode.com/" + year + "/day/" + day + "/input"
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		return "", err
	}
	req.AddCookie(cookie)

	client := &http.Client{}

	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	bodyString := ""
	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := io.ReadAll(resp.Body)
		if err != nil {
			return "", err
		}
		bodyString = string(bodyBytes)
	}
	return bodyString, nil
}
