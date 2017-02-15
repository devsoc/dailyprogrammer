#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <stdlib.h>
#include <vector>
#include <locale>
using namespace std;


struct atom{
	int no;
	string symbol;
	string name;
	double weight;
	bool operator<(const atom &second){
		return weight > second.weight;
	}
};

vector<atom> atoms;

void readCSV(){
	atom a;
	int index;
	string l;
	ifstream f;
	f.open("../atomic.csv");
	string temp;
	getline(f, temp); // Headers
	while(getline(f, temp)){
		index = temp.find(",");
		l = temp.substr(0,index);
		a.no = stoul(l.c_str());
		temp = temp.substr(index+3, temp.length());
		index = temp.find(" ");
		l = temp.substr(0, index);
		a.symbol = l;
		temp = temp.substr(index+5, temp.length());
		index = temp.find(" ");
		int index1 = temp.find(",");
		if(index1 > index)
			l = temp.substr(0, index);
		else
			l = temp.substr(0, index1 - 1);
		transform(l.begin(), l.end(), l.begin(), ::tolower);
		a.name = l;
		index = temp.find(",\" ");
		temp = temp.substr(index+3, temp.length()-1);
		a.weight = stod(temp.c_str());
		atoms.push_back(a);
	}
	sort(atoms.begin(), atoms.end());
	//for(int i=0;i<atoms.size();i++)
	//	cout<<"\n"<<atoms[i].no<<"::"<<atoms[i].symbol<<"::"<<atoms[i].name<<"::"<<atoms[i].weight;
}

int findElem(string a){
	a[0] = toupper(a[0]);
	for(int i=0;i<atoms.size();i++)
		if(a == atoms[i].symbol)
			return i;
	return -1;
}

string expand(string test){
	string result = "";
	string elems[20], sym[20];
	int sym_len=0, elem_len=0;
	for(int i=0; i<test.length();){
		int index = findElem(test.substr(i,1));
		if(index != -1){
			sym[sym_len++] = atoms[index].symbol;
			elems[elem_len++] = atoms[index].name;
			++i;
		}
		else{
			index = findElem(test.substr(i,2));
			if(index == -1)	return (string)"Is this a new Element?\n";
			i+=2;
			sym[sym_len++] = atoms[index].symbol;
			elems[elem_len++] = atoms[index].name;
		}
	}
	for(int i=0;i<sym_len;i++)
		result += sym[i];
	result += " (";
	for(int i=0;i<elem_len;i++)
		result += elems[i]+", ";
	result = result.substr(0, result.length()-2) + ")";
	return result;
}


int main(){
	readCSV();
	string tests[] = {"functions", "bacon", "poison", "sickness",
				"ticklish"};
	for(int i=0;i<5;i++)
		cout<<expand(tests[i])<<"\n";
	return 0;
}
