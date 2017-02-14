#include <iostream>
#include <string>
#include <math.h>
using namespace std;

int len = 0;

bool redundant(int** filtered, int len, int index){
	for(int i=0;i<len;i++){
		if(filtered[i][0]==index || filtered[i][1]==index)
			return true;
	}
	return false;
}

int** getPairs(string exp){
	int** pairs = new int*[20];
	for(int z=0; z<20; z++)	pairs[z] = new int[2];
	int** a = new int*[20];
	for(int z=0; z<20; z++)	a[z] = new int[2];
	int k=0,l=0,s=0;
	for(int j=0; j<exp.length(); j++){
		//cout<<"\n"<<exp[j];
		if(exp[j] == '('){
			pairs[k][0] = j;
			pairs[k][1] = -1;
			k++;
			l++;
		}
		else if(exp[j] == ')'){
			k--;
			pairs[k][1] = j;
			//cout<<"::"<<k;
			a[s][0] = pairs[k][0];
			a[s][1] = pairs[k][1];
			s++;
			//cout<<"\n"<<pairs[k][0]<<" :: "<<pairs[k][1];
		}
	}
	//cout<<"\n\n\n\nFor exp :: "<<exp;
	//cout<<l;
	len = l;
	//for(int i=0; i<len; i++)cout<<"\n"<<a[i][0]<<" :: "<<a[i][1];
	return a;
}


string removeExtra(string exp){
	int** filtered = new int*[20];
	for(int z=0;z<2;z++)	filtered[z] = new int[2];
	int** a = getPairs(exp);
	int f_len=0;
	//cout<<"\n"<<len<<"\n";
	//for(int i=0; i<len; i++)	cout<<"\n"<<a[i][0]<<" :: "<<a[i][1];
	for(int i=0, z=0; i<len; i++){
		if(a[i][0]+1==a[i][1]){
			filtered[z][0] = a[i][0];
			filtered[z][1] = a[i][1];
			z++;
			f_len = z;
			continue;
		}
		for(int j=i;j<len;j++){
			if(abs(a[i][0]-a[j][0])==1 && abs(a[i][1]-a[j][1])==1){
				filtered[z][0] = a[i][0];
				filtered[z][1] = a[i][1];
				z++;
				f_len = z;
			}
		}
	}
	string newExp = "";
	for(int i=0,z=0;i<exp.length();i++){
		if(!redundant(filtered, f_len, i))
			newExp += exp[i];
	}
	delete a;
	delete filtered;
	return newExp;
}

int main(){
	string tests[] = {"((a((bc)(de)))f)", "(((zbcd)(((e)fg))))",
	       	"ab((c))", "()", "((fgh()()()))", "()(abc())"};
	int num_of_tests = sizeof(tests)/sizeof(tests[0]);
	for(int i=0; i<num_of_tests; i++)
		cout<<removeExtra(tests[i])<<"\n";
	return 0;
}
