package main

import (
	"fmt"
	"os"
	"strings"
)

var (
	testFile = "day12/test/t2.txt"
	rowMax   = 0
	colMax   = 0
)

type Box struct {
	Row int
	Col int
}

type Garden struct {
	garden [][]string
}

func (g *Garden) TypeInBox(b *Box) string {
	t := ""
	if b.Col <= colMax && b.Col >= 0 && b.Row <= rowMax && b.Row >= 0 {
		t = g.garden[b.Row][b.Col]
	}
	return t
}

type Region struct {
	Type  string
	Boxes []*Box
}

func calc3(cur *Box, sameAjas, otherAjas, sameDiags, otherDiags, checked []*Box) int {
	// on a wall
	if len(sameAjas)+len(otherAjas)+len(sameDiags)+len(otherDiags) == 5 {
		return 4
	}
	c := 2
	for _, diag := range sameDiags {
		if !contains(checked, diag) {
			c++
		}
	}
	return c
}

func calc2(cur *Box, sameAjas, otherAjas, sameDiags, otherDiags, checked []*Box) int {
	// in a corner
	if len(sameAjas)+len(otherAjas)+len(sameDiags)+len(otherDiags) == 3 {
		return 4
	}

	c := 0
	// if ajas[0].Row == ajas[1].Row || ajas[0].Col == ajas[1].Col {
	// 	// plus one per unchecked diag
	// 	for _, diag := range diags {
	// 		if !contains(checked, diag) {
	// 			c++
	// 		}
	// 	}
	// 	return c
	// }
	// c = 1
	// for _, diag := range diags {
	// 	if !contains(checked, diag) {
	// 		c++
	// 	}
	// }
	return c
}

func calc1(ajas, diags []*Box) int {
	if len(ajas)+len(diags) == 7 {
		return 1
	}
	return 0
}

func (r *Region) Sides(g *Garden) int {
	count := 0
	checked := []*Box{}
	for _, box := range r.Boxes {
		sameAjas, otherAjas := getAjas(g, box)
		sameDiags, otherDiags := getDiags(g, box)
		// 4 ajas = 4
		if len(otherAjas) == 4 {
			count += 4
		}
		// 3 ajas = 2 + count diags if diags not already checked
		if len(otherAjas) == 3 {
			count += calc3(box, sameAjas, otherAjas, sameDiags, otherDiags, checked)
		}
		// 2 ajas = 1 + count diags if diags not checked OR 0 if ajas in a line
		// if len(otherAjas) == 2 {
		// 	count += calc2(box, ajas, diags, checked)
		// }
		// // 1 aja = 0 unless it has 7 sametype neigbors
		// if len(otherAjas) == 1 {
		// 	count += calc1(ajas, diags)
		// }
		checked = append(checked, box)
	}
	return count
}

func (r *Region) Perimeter(g *Garden) int {
	perimeter := 0
	for _, box := range r.Boxes {
		c, _ := countAjas(g, box)
		perimeter += c
	}

	return perimeter
}

func getDiags(g *Garden, b *Box) ([]*Box, []*Box) {
	sameType := []*Box{}
	otherType := []*Box{}
	diags := []*Box{
		{
			Row: b.Row - 1,
			Col: b.Col - 1,
		},
		{
			Row: b.Row + 1,
			Col: b.Col + 1,
		},
		{
			Row: b.Row - 1,
			Col: b.Col + 1,
		},
		{
			Row: b.Row + 1,
			Col: b.Col - 1,
		},
	}
	for _, diag := range diags {
		if g.TypeInBox(diag) == g.TypeInBox(b) {
			sameType = append(sameType, diag)
		} else {
			otherType = append(otherType, diag)
		}
	}
	return sameType, otherType
}

func getAjas(g *Garden, b *Box) ([]*Box, []*Box) {
	sameType := []*Box{}
	otherType := []*Box{}
	ajas := []*Box{
		{
			Row: b.Row,
			Col: b.Col - 1,
		},
		{
			Row: b.Row,
			Col: b.Col + 1,
		},
		{
			Row: b.Row - 1,
			Col: b.Col,
		},
		{
			Row: b.Row + 1,
			Col: b.Col,
		},
	}
	for _, aja := range ajas {
		if g.TypeInBox(aja) == g.TypeInBox(b) {
			sameType = append(sameType, aja)
		} else {
			otherType = append(otherType, aja)
		}
	}
	return sameType, otherType

}

func countAjas(g *Garden, b *Box) (int, []*Box) {
	count := 0
	sameType := []*Box{}
	ajas := []*Box{
		{
			Row: b.Row,
			Col: b.Col - 1,
		},
		{
			Row: b.Row,
			Col: b.Col + 1,
		},
		{
			Row: b.Row - 1,
			Col: b.Col,
		},
		{
			Row: b.Row + 1,
			Col: b.Col,
		},
	}
	for _, aja := range ajas {
		if g.TypeInBox(aja) != g.TypeInBox(b) {
			count++
		} else {
			sameType = append(sameType, aja)
		}
	}
	return count, sameType

}

func parseData(file string) [][]string {
	data, err := os.ReadFile(file)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return nil
	}
	dataS := strings.Split(strings.TrimSpace(string(data)), "\n")
	gardens := [][]string{}
	for _, line := range dataS {
		gardens = append(gardens, strings.Split(line, ""))
	}

	return gardens
}

func (g *Garden) PrintGarden() {
	for _, row := range g.garden {
		for _, col := range row {
			fmt.Printf(col)
		}
		fmt.Printf("\n")
	}
}

func (g *Garden) SetBounds() {
	rowMax = len(g.garden) - 1
	colMax = len(g.garden[0]) - 1
}

func contains(l []*Box, t *Box) bool {
	for _, b := range l {
		if b.Row == t.Row && b.Col == t.Col {
			return true
		}
	}
	return false
}

func fillRegion(box *Box, region *Region, g *Garden) {
	ajas := []*Box{
		{
			Row: box.Row,
			Col: box.Col - 1,
		},
		{
			Row: box.Row,
			Col: box.Col + 1,
		},
		{
			Row: box.Row - 1,
			Col: box.Col,
		},
		{
			Row: box.Row + 1,
			Col: box.Col,
		},
	}

	for _, aja := range ajas {
		if g.TypeInBox(aja) == region.Type && !contains(region.Boxes, aja) {
			region.Boxes = append(region.Boxes, aja)
			fillRegion(aja, region, g)
		}
	}
}

func getRegions(g *Garden) []*Region {
	regions := []*Region{}
	mapped := []*Box{}

	for rowI, row := range g.garden {
		for colI, col := range row {
			newBox := Box{
				Row: rowI,
				Col: colI,
			}
			if !contains(mapped, &newBox) {
				newRegion := Region{
					Type:  col,
					Boxes: []*Box{&newBox},
				}
				fillRegion(&newBox, &newRegion, g)
				regions = append(regions, &newRegion)
				mapped = append(mapped, newRegion.Boxes...)
			}
		}
	}

	return regions
}

func part1() int {
	garden := Garden{
		garden: parseData(testFile),
	}
	garden.SetBounds()

	regions := getRegions(&garden)
	price := 0
	for _, region := range regions {
		p := region.Perimeter(&garden)
		a := len(region.Boxes)
		price += a * p
	}
	return price
}

func part2() int {
	garden := Garden{
		garden: parseData(testFile),
	}
	garden.SetBounds()

	regions := getRegions(&garden)
	price := 0
	for _, region := range regions {
		s := region.Sides(&garden)
		a := len(region.Boxes)
		price += s * a
		fmt.Printf("(%v) : %d * %d = %d\n", region.Type, a, s, s*a)
	}

	return price
}

func main() {
	fmt.Printf("Part 1: %d\n", part1())
	fmt.Printf("Part 2: %d\n", part2())
}
