#!/usr/bin/env python3
"""
Resume Updater Script - ENHANCED VERSION
Intelligently updates your DevOps resume based on job requirements
"""

from docx import Document
from docx.shared import Pt
import os
import sys
import re
from datetime import datetime

class ResumeUpdater:
    def __init__(self, original_resume_path, output_dir):
        self.original_resume_path = original_resume_path
        self.output_dir = output_dir
        self.doc = None
        
        self.tech_terms = [
            'AWS', 'Azure', 'GCP', 'Google Cloud',
            'ECS', 'Fargate', 'Lambda', 'EC2', 'S3', 'VPC', 'ELB', 'CloudFormation',
            'Aurora', 'PostgreSQL', 'MySQL', 'DynamoDB', 'MongoDB', 'RDS',
            'Kubernetes', 'Docker', 'OpenShift', 'Helm', 'ArgoCD', 'Kustomize',
            'Jenkins', 'GitLab CI/CD', 'GitHub Actions', 'Tekton', 'Bamboo', 'TeamCity',
            'Terraform', 'Pulumi', 'Ansible', 'Chef', 'Puppet',
            'Prometheus', 'Grafana', 'DataDog', 'Splunk', 'ELK', 'Nagios',
            'Python', 'Bash', 'Shell', 'Groovy', 'Go', 'Ruby', 'Perl',
            'Apache Kafka', 'Kinesis', 'RabbitMQ', 'Redis',
            'Nginx', 'Apache', 'Tomcat', 'JBoss', 'WebSphere',
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN',
            'JIRA', 'Confluence', 'ServiceNow',
            'Linux', 'RHEL', 'CentOS', 'Ubuntu', 'Debian',
            'Maven', 'Ant', 'Gradle', 'npm', 'yarn',
            'Istio', 'Linkerd', 'Flux', 'Crossplane',
            'SonarQube', 'Trivy', 'Snyk', 'Checkmarx',
            'CI/CD', 'DevOps', 'GitOps', 'DevSecOps', 'SRE',
            'REST API', 'GraphQL', 'gRPC', 'WebSockets',
            'Microservices', 'BFF', 'API Gateway',
            'SAFe Agile', 'Scrum', 'Kanban',
            'SSL', 'TLS', 'mTLS', 'OAuth', 'SAML',
            'CloudWatch', 'Application Insights', 'New Relic',
            'Selenium', 'JUnit', 'TestNG', 'pytest',
            'YAML', 'JSON', 'XML', 'HCL'
        ]
    
    def load_resume(self):
        """Load the original resume"""
        if not os.path.exists(self.original_resume_path):
            print(f'Error: Resume file not found at {self.original_resume_path}')
            sys.exit(1)
        
        self.doc = Document(self.original_resume_path)
        print(f'✓ Loaded resume: {os.path.basename(self.original_resume_path)}')
    
    def extract_all_skills(self, job_description):
        """Extract ALL skills dynamically from job description"""
        try:
            found_skills = set()
            
            # Extract skills with "experience", "expertise", etc
            phrases = re.findall(
                r'(?:experience|expertise|proficiency|skill|knowledge|familiarity)[\s\w]*?(?:in|with)[\s]*([A-Za-z\s\-/+\.()]{3,80}?)(?:,|and|or|;|\.|$)',
                job_description,
                re.IGNORECASE
            )
            
            for phrase in phrases:
                cleaned = phrase.strip()
                if len(cleaned) > 2:
                    found_skills.add(cleaned)
            
            # Extract tools/frameworks/platforms
            tools = re.findall(
                r'([A-Za-z0-9\s\-/+\.()]+?)(?:\s+tools?|\s+frameworks?|\s+platforms?)',
                job_description,
                re.IGNORECASE
            )
            
            for tool in tools:
                cleaned = tool.strip()
                if len(cleaned) > 2:
                    found_skills.add(cleaned)
            
            # Extract capabilities
            capabilities = re.findall(
                r'(?:ability|capable|expertise)[\s\w]*?(?:to|in|with)[\s]*([A-Za-z\s\-/+\.()]{3,80}?)(?:,|and|or|;|\.|$)',
                job_description,
                re.IGNORECASE
            )
            
            for capability in capabilities:
                cleaned = capability.strip()
                if len(cleaned) > 2:
                    found_skills.add(cleaned)
            
            # Extract capitalized terms
            technical_terms = re.findall(
                r'\b([A-Z][a-zA-Z0-9\-/+\.]*(?:\s+[A-Z][a-zA-Z0-9\-/+\.]*)*)\b',
                job_description
            )
            
            for term in technical_terms:
                if len(term) > 2 and term not in ['The', 'This', 'Job', 'Role', 'Must', 'Should', 'Will', 'Have']:
                    found_skills.add(term)
            
            # Clean up
            final_skills = set()
            for skill in found_skills:
                cleaned = skill.strip().rstrip(',.')
                if cleaned and len(cleaned) > 2:
                    final_skills.add(cleaned)
            
            return sorted(list(final_skills))
        
        except Exception as e:
            print(f"Error extracting skills: {e}")
            return []
    
    def find_missing_skills(self, all_skills, resume_text):
        """Find skills NOT in resume"""
        try:
            missing = []
            for skill in all_skills:
                if not re.search(rf'\b{re.escape(skill)}\b', resume_text, re.IGNORECASE):
                    missing.append(skill)
            return missing
        except Exception as e:
            print(f"Error finding missing skills: {e}")
            return []
    
    def generate_missing_skills_bullets(self, missing_skills, job_description):
        """Generate ONE bullet per missing skill"""
        bullets = []
        
        if not missing_skills:
            return bullets
        
        print(f'\n✨ Generating bullets for {len(missing_skills)} missing skills...')
        
        skill_templates = {
            'AWS Organizations': 'Implemented AWS Organizations and Service Control Policies (SCPs) to enforce security governance across multi-account AWS environments',
            'AWS Config': 'Configured AWS Config rules for automated compliance monitoring and infrastructure validation',
            'AWS Security Hub': 'Deployed AWS Security Hub for centralized threat detection and compliance status aggregation',
            'AWS IAM': 'Designed fine-grained IAM policies enforcing least-privilege access principles across AWS resources',
            'AWS cost optimization': 'Optimized AWS infrastructure costs through reserved instances, spot instances, and right-sizing analysis',
            'IQ scripts': 'Developed and maintained IQ scripts for automated security validation and policy compliance verification',
            'Service Control Policies': 'Implemented Service Control Policies (SCPs) for multi-account governance and security enforcement',
            'SCPs': 'Configured SCPs for centralized policy management and compliance enforcement across organizations',
            'Terraform': 'Managed infrastructure automation and version control using Terraform for Infrastructure-as-Code deployment',
            'CloudFormation': 'Designed AWS CloudFormation templates for Infrastructure-as-Code automation and consistent environment provisioning',
            'Pulumi': 'Implemented Pulumi for programmatic infrastructure definition and multi-cloud resource provisioning',
            'CDK': 'Utilized AWS CDK for infrastructure definition using familiar programming languages',
            'Python': 'Developed Python automation scripts for infrastructure management and CI/CD pipeline orchestration',
            'Bash': 'Wrote Bash scripts for system automation and DevOps workflow optimization',
            'Jenkins': 'Implemented Jenkins CI/CD pipelines for automated build, test, and production deployment',
            'ArgoCD': 'Deployed and maintained ArgoCD for GitOps-based continuous deployment and infrastructure-as-code synchronization',
            'GitHub Actions': 'Configured GitHub Actions workflows for automated testing, building, and deployment',
            'GitLab CI': 'Implemented GitLab CI/CD pipelines for automated software delivery across multiple environments',
            'Kubernetes': 'Architected and managed Kubernetes clusters for container orchestration and microservices deployment',
            'Docker': 'Containerized applications using Docker for consistent multi-environment deployment and reduced deployment complexity',
            'Helm': 'Utilized Helm for Kubernetes package management and templated application deployments',
            'DevSecOps': 'Integrated security practices into DevOps workflows with automated scanning and compliance verification',
            'CI/CD pipelines': 'Designed comprehensive CI/CD pipelines for automated testing and production deployment',
            'Microservices': 'Architected and deployed microservices-based applications for improved scalability and independent service management',
        }
        
        try:
            for skill in missing_skills:
                if skill in skill_templates:
                    bullet = f'•   {skill_templates[skill]}'
                    bullets.append(bullet)
                else:
                    found = False
                    for template_skill, template_bullet in skill_templates.items():
                        if skill.lower() in template_skill.lower() or template_skill.lower() in skill.lower():
                            bullet = f'•   {template_bullet}'
                            bullets.append(bullet)
                            found = True
                            break
                    
                    if not found:
                        bullet = f'•   Demonstrated hands-on experience with {skill} in production environments'
                        bullets.append(bullet)
            
            print(f'  ✓ Generated {len(bullets)} bullets')
            return bullets
        
        except Exception as e:
            print(f"Error generating bullets: {e}")
            return []
    
    def parse_requirements(self, requirements_text):
        """Parse job requirements"""
        print('\n📋 Analyzing requirements...')
        
        requirements = {
            'cloud_services': [],
            'containers': [],
            'cicd_tools': [],
            'programming': [],
            'databases': [],
            'monitoring': [],
            'messaging': [],
            'other_skills': [],
            'methodologies': [],
            'missing_skills': [],
            'all_extracted_skills': []
        }
        
        try:
            all_extracted_skills = self.extract_all_skills(requirements_text)
            requirements['all_extracted_skills'] = all_extracted_skills
            print(f'✓ Found {len(all_extracted_skills)} total skills')
            
            resume_text = '\n'.join([p.text for p in self.doc.paragraphs])
            missing_skills = self.find_missing_skills(all_extracted_skills, resume_text)
            requirements['missing_skills'] = missing_skills[:20]
            print(f'✓ Missing: {len(missing_skills)} skills')
            
            req_lower = requirements_text.lower()
            
            if 'ecs' in req_lower or 'fargate' in req_lower:
                requirements['cloud_services'].append('ECS Fargate')
            if 'lambda' in req_lower or 'serverless' in req_lower:
                requirements['cloud_services'].append('Lambda')
            if 'aurora' in req_lower:
                requirements['cloud_services'].append('Aurora PostgreSQL')
            if 'dynamodb' in req_lower:
                requirements['cloud_services'].append('DynamoDB')
            if 'kinesis' in req_lower:
                requirements['cloud_services'].append('Kinesis')
            
            if 'kubernetes' in req_lower or 'k8s' in req_lower:
                requirements['containers'].append('Kubernetes')
            if 'docker' in req_lower:
                requirements['containers'].append('Docker')
            if 'helm' in req_lower:
                requirements['containers'].append('Helm')
            if 'argocd' in req_lower:
                requirements['containers'].append('ArgoCD')
            
            if 'jenkins' in req_lower:
                requirements['cicd_tools'].append('Jenkins')
            if 'github actions' in req_lower:
                requirements['cicd_tools'].append('GitHub Actions')
            if 'gitlab' in req_lower:
                requirements['cicd_tools'].append('GitLab CI/CD')
            
            if 'postgres' in req_lower:
                requirements['databases'].append('PostgreSQL')
            if 'mysql' in req_lower:
                requirements['databases'].append('MySQL')
            if 'mongodb' in req_lower:
                requirements['databases'].append('MongoDB')
            
            if 'kafka' in req_lower:
                requirements['messaging'].append('Apache Kafka')
            
            if 'prometheus' in req_lower:
                requirements['monitoring'].append('Prometheus')
            if 'grafana' in req_lower:
                requirements['monitoring'].append('Grafana')
            
            if 'microservices' in req_lower:
                requirements['other_skills'].append('microservices')
            if 'bff' in req_lower:
                requirements['other_skills'].append('BFF')
            
            if 'safe' in req_lower:
                requirements['methodologies'].append('SAFe Agile')
            
            return requirements
        
        except Exception as e:
            print(f"Error parsing requirements: {e}")
            return requirements
    
    def make_selective_bold(self, paragraph, tech_list):
        """Make tech terms bold"""
        try:
            full_text = paragraph.text
            for run in paragraph.runs:
                run.text = ''
            
            sorted_tech = sorted(tech_list, key=len, reverse=True)
            remaining_text = full_text
            
            while remaining_text:
                earliest_pos = len(remaining_text)
                earliest_term = None
                
                for term in sorted_tech:
                    pos = remaining_text.find(term)
                    if pos != -1 and pos < earliest_pos:
                        earliest_pos = pos
                        earliest_term = term
                
                if earliest_term:
                    if earliest_pos > 0:
                        run = paragraph.add_run(remaining_text[:earliest_pos])
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(11)
                        run.font.bold = False
                    
                    tech_run = paragraph.add_run(earliest_term)
                    tech_run.font.name = 'Times New Roman'
                    tech_run.font.size = Pt(11)
                    tech_run.font.bold = True
                    
                    remaining_text = remaining_text[earliest_pos + len(earliest_term):]
                else:
                    if remaining_text:
                        run = paragraph.add_run(remaining_text)
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(11)
                        run.font.bold = False
                    break
        except Exception as e:
            print(f"Error making bold: {e}")
    
    def insert_summary_bullets(self, bullets):
        """Insert bullets into summary"""
        print(f'\n✏️  Adding {len(bullets)} bullets to Summary...')
        
        try:
            insertion_index = None
            for i, para in enumerate(self.doc.paragraphs):
                if 'Implemented reproducible build workflows by integrating' in para.text and 'Conan' in para.text:
                    insertion_index = i + 1
                    break
            
            if insertion_index:
                reference_para = self.doc.paragraphs[insertion_index]
                
                for bullet_text in reversed(bullets):
                    new_para = reference_para.insert_paragraph_before()
                    new_para.text = bullet_text
                    new_para.paragraph_format.left_indent = reference_para.paragraph_format.left_indent
                    new_para.paragraph_format.first_line_indent = reference_para.paragraph_format.first_line_indent
                    self.make_selective_bold(new_para, self.tech_terms)
                
                print('  ✓ Summary updated')
                return True
            else:
                print('  ✗ Could not find insertion point')
                return False
        except Exception as e:
            print(f"Error inserting summary bullets: {e}")
            return False
    
    def insert_job_bullets(self, bullets, company_keyword, year):
        """Insert bullets into job section"""
        print(f'\n✏️  Adding {len(bullets)} bullets to {company_keyword}...')
        
        try:
            for i, para in enumerate(self.doc.paragraphs):
                if company_keyword in para.text and year in para.text:
                    for j in range(i, min(i+60, len(self.doc.paragraphs))):
                        para_text = self.doc.paragraphs[j].text
                        
                        if ('Tekton pipelines with ArgoCD' in para_text or
                            'Integrated Tekton pipelines' in para_text or
                            'Kubernetes for the runtime environment' in para_text or
                            'Flux for GitOps-based cluster state' in para_text):
                            
                            insert_at = j + 1
                            ref_para = self.doc.paragraphs[insert_at]
                            
                            for addition in reversed(bullets):
                                new_p = ref_para.insert_paragraph_before()
                                new_p.text = addition
                                new_p.paragraph_format.left_indent = ref_para.paragraph_format.left_indent
                                new_p.paragraph_format.first_line_indent = ref_para.paragraph_format.first_line_indent
                                self.make_selective_bold(new_p, self.tech_terms)
                            
                            print(f'  ✓ {company_keyword} updated')
                            return True
                    break
            
            print(f'  ✗ Could not find {company_keyword}')
            return False
        except Exception as e:
            print(f"Error inserting job bullets: {e}")
            return False
    
    def update_technical_skills(self, requirements):
        """Update technical skills table"""
        print('\n✏️  Updating Technical Skills...')
        
        try:
            updates_made = 0
            
            for table in self.doc.tables:
                for row in table.rows:
                    cells = row.cells
                    if len(cells) >= 2:
                        category = cells[0].text.strip()
                        content = cells[1].text.strip()
                        
                        if 'Cloud Technologies' in category and requirements['cloud_services']:
                            new_services = [svc for svc in requirements['cloud_services'] if svc not in content]
                            if new_services and 'Amazon Web Services' in content:
                                cells[1].text = content + ', ' + ', '.join(new_services)
                                updates_made += 1
                        
                        elif 'CI/CD Tools' in category and requirements['cicd_tools']:
                            new_tools = [tool for tool in requirements['cicd_tools'] if tool not in content]
                            if new_tools:
                                cells[1].text = content + ', ' + ', '.join(new_tools)
                                updates_made += 1
                        
                        elif 'Databases' in category and requirements['databases']:
                            new_dbs = [db for db in requirements['databases'] if db not in content]
                            if new_dbs:
                                cells[1].text = content + ', ' + ', '.join(new_dbs)
                                updates_made += 1
            
            print(f'  ✓ Technical Skills updated ({updates_made} changes)')
        except Exception as e:
            print(f"Error updating skills: {e}")
    
    def save_resume(self, output_path=None):
        """Save resume"""
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(self.original_resume_path))[0]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'{base_name}_Updated_{timestamp}.docx'
            output_path = os.path.join(self.output_dir, filename)
        
        os.makedirs(self.output_dir, exist_ok=True)
        self.doc.save(output_path)
        print(f'\n✅ Saved: {os.path.basename(output_path)}')
        return output_path
    
    def update_resume(self, requirements_text):
        """Main update method"""
        print('\n' + '='*60)
        print('RESUME UPDATER - GUARANTEED SKILL COVERAGE')
        print('='*60)
        
        try:
            self.load_resume()
            requirements = self.parse_requirements(requirements_text)
            
            if not any([requirements.get('missing_skills'), requirements.get('cloud_services')]):
                print('\n⚠️  No relevant skills found')
                return None
            
            summary_bullets = []
            job_bullets = []
            
            if requirements.get('missing_skills'):
                job_bullets = self.generate_missing_skills_bullets(
                    requirements['missing_skills'],
                    requirements_text
                )
            
            self.insert_summary_bullets(summary_bullets)
            
            if job_bullets:
                self.insert_job_bullets(job_bullets, 'Early Warning', '2024')
            
            self.update_technical_skills(requirements)
            output_path = self.save_resume()
            
            print('\n' + '='*60)
            print('✅ UPDATE COMPLETE!')
            print('='*60)
            
            return output_path
        
        except Exception as e:
            print(f'\n❌ Error: {e}')
            import traceback
            traceback.print_exc()
            return None


def main():
    """Main function"""
    print('='*60)
    print('RESUME UPDATER')
    print('='*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = '/Users/gokul/Desktop/Devops 12+/edited resumes'
    
    print(f'Output: {output_dir}\n')
    
    requirements_file = os.path.join(script_dir, 'job_requirement.txt')
    
    if not os.path.exists(requirements_file):
        print('❌ job_requirement.txt not found!')
        sys.exit(1)
    
    print('✓ Found job_requirement.txt')
    
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements_text = f.read()
    
    if not requirements_text.strip():
        print('❌ job_requirement.txt is empty!')
        sys.exit(1)
    
    print(f'✓ Loaded requirements')
    
    resume_files = [f for f in os.listdir(script_dir) if f.endswith('.docx') and 'Updated' not in f and '~$' not in f]
    
    if not resume_files:
        print('❌ No resume found!')
        sys.exit(1)
    
    if len(resume_files) == 1:
        resume_file = resume_files[0]
        print(f'✓ Found resume: {resume_file}')
    else:
        print('Multiple resumes found:')
        for i, f in enumerate(resume_files, 1):
            print(f'  {i}. {f}')
        choice = input('\nSelect: ')
        try:
            resume_file = resume_files[int(choice) - 1]
        except (ValueError, IndexError):
            print('Invalid!')
            sys.exit(1)
    
    resume_path = os.path.join(script_dir, resume_file)
    
    try:
        updater = ResumeUpdater(resume_path, output_dir)
        output_path = updater.update_resume(requirements_text)
        
        if output_path:
            print(f'\n📄 Resume: {output_path}')
    
    except Exception as e:
        print(f'\n❌ Error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
