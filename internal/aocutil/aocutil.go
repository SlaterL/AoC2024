package aocutil

import "strconv"

func LenOfInt(i int) int {
	s := strconv.Itoa(i)
	return len(s)
}

func IsEven(num int) bool {
	return num%2 == 0
}

type Node struct {
	Index int
	Value int
	Next  *Node
}

type LinkedList struct {
	Head *Node
	tail *Node
}

func NewLinkedList() LinkedList {
	return LinkedList{
		Head: nil,
		tail: nil,
	}
}

func (l *LinkedList) Append(i int) {
	n := &Node{
		Value: i,
		Next:  nil,
	}
	if l.Head == nil {
		n.Index = 0
		l.Head = n
		l.tail = n
		return
	}

	n.Index = l.tail.Index + 1
	l.tail.Next = n
	l.tail = n
}

func (l *LinkedList) Length() int {
	return l.tail.Index + 1
}

func (l *LinkedList) Str() string {
	s := ""
	cur := l.Head
	for cur != nil {
		s = s + " " + strconv.Itoa(cur.Value)
		cur = cur.Next
	}
	return s
}
